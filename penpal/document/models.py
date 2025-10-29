import uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    soft_delete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['name', 'slug']),
            models.Index(fields=['soft_delete']),
        ]
        db_table = 'tags'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Tag.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField(help_text="HTML content for TipTap editor")
    content_json = models.JSONField(default=dict, blank=True)
    block_note_content = models.JSONField(default=dict, blank=True)

    document_type = models.CharField(
        max_length=50,
        choices=[
            ('blog', 'Blog Post'),
            ('tutorial', 'Tutorial'),
            ('tech-doc', 'Technical Documentation'),
            ('marketing', 'Marketing Content'),
            ('srs', 'Software Requirements Specification'),
            ('other', 'Other')
        ],
        default='other'
    )

    editor_type = models.CharField(
        max_length=20,
        choices=[
            ('tiptap', 'TipTap'),
            ('blocknote', 'BlockNote'),
            ('hybrid', 'Hybrid'),
            ('markdown', 'Markdown'),
            ('other', 'Other')
        ],
        default='other'
    )

    is_public = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=False)
    allow_sharing = models.BooleanField(default=False)
    allow_editing = models.BooleanField(default=False)

    word_count = models.PositiveIntegerField(default=0)
    read_time = models.CharField(max_length=20, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('archived', 'Archived'),
        ],
        default='draft'
    )

    tags = models.ManyToManyField('Tag', related_name='tagged_documents', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    soft_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['author', 'status']),
            models.Index(fields=['document_type', 'status']),
            models.Index(fields=['editor_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['soft_delete']),
        ]
        unique_together = ('author', 'title')
        db_table = 'documents'


    def save(self, *args, **kwargs):
        if self.content:
            self.word_count = len(self.content.split())
            self.read_time = f"{max(1, self.word_count // 200)} min"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.author.username})"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    soft_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['document', 'author']),
            models.Index(fields=['soft_delete']),
        ]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(body=""),
                name="comment_body_not_empty"
            )
        ]
        db_table = 'comments'

    def __str__(self):
        return f"{self.body[:10]} - ({self.document.title[:10]}) - ({self.author.username})"

class MediaAsset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='media_assets')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_assets')

    file_type = models.CharField(
        max_length=20,
        choices=[
            ('image', 'Image'),
            ('video', 'Video'),
            ('file', 'File')]
    )
    file = models.FileField(upload_to='media_assets/')
    # `url` (CharField or URLField; pre-signed/external)
    url = models.URLField(blank=True)
    meta_data = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    soft_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['document', 'owner']),
            models.Index(fields=['soft_delete']),
        ]
        db_table = 'media_assets'
        # If you use external storage (e.g., S3), allow file or url but not both empty.
        constraints = [
            models.CheckConstraint(
                check=(models.Q(file__isnull=False) | models.Q(url__isnull=False)),
                name="media_asset_requires_file_or_url"
            )
        ]

    def __str__(self):
        filename = self.file.name.split('/')[-1] if self.file else "No file"
        return f"{filename} ({self.file_type}) - {self.document.title[:20]}"

