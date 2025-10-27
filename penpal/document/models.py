# models.py
import uuid

from django.contrib.auth.models import User
from django.db import models


class Document(models.Model):
    # Core identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, help_text="Document title")

    # Content fields
    content = models.TextField(help_text="HTML content for TipTap editor")
    block_note_content = models.JSONField(default=list, help_text="BlockNote structured content")

    # Metadata
    description = models.TextField(blank=True, help_text="Document description/summary")
    document_type = models.CharField(
        max_length=50,
        choices=[
            ('blog', 'Blog Post'),
            ('tutorial', 'Tutorial'),
            ('tech-doc', 'Technical Documentation'),
            ('marketing', 'Marketing Content'),
        ],
        default='blog'
    )

    # Editor configuration
    editor_type = models.CharField(
        max_length=20,
        choices=[
            ('tiptap', 'TipTap'),
            ('blocknote', 'BlockNote'),
            ('hybrid', 'Hybrid'),
        ],
        default='hybrid'
    )

    # Status and workflow
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('archived', 'Archived'),
        ],
        default='draft'
    )

    # Ownership and permissions
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Analytics
    word_count = models.PositiveIntegerField(default=0)
    read_time = models.CharField(max_length=20, blank=True, help_text="Estimated read time")

    # Organization
    tags = models.JSONField(default=list, help_text="Document tags")

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['author', 'status']),
            models.Index(fields=['document_type', 'status']),
            models.Index(fields=['editor_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title