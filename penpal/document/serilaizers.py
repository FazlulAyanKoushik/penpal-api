# serializers.py
from django.db import IntegrityError
from rest_framework import serializers

from .models import Document, Tag, Comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'author_username',
            'body', 'created_at', 'updated_at', 'soft_delete'
        ]
        read_only_fields = ['id', 'author', 'author_username', 'created_at', 'updated_at']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class DocumentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, source='tags', required=False
    )

    class Meta:
        model = Document
        fields = [
            'id', 'author', 'author_username',
            'title', 'description', 'content', 'content_json', 'block_note_content',
            'document_type', 'editor_type', 'is_public',
            'allow_comments', 'allow_sharing', 'allow_editing',
            'word_count', 'read_time', 'status', 'tags', 'tag_ids',
            'created_at', 'updated_at', 'soft_delete'
            ]
        read_only_fields = ['id', 'author', 'word_count', 'read_time', 'created_at', 'updated_at']

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value.strip()

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty")
        return value

    def validate_tags(self, value):
        if value and not isinstance(value, list):
            raise serializers.ValidationError("Tags must be a list")
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        try:
            document = Document.objects.create(**validated_data)
            if tags:
                document.tags.set(tags)
            return document
        except IntegrityError as e:
            raise serializers.ValidationError({"title": "You already have a document with this title."})


class DocumentListSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'author', 'author_username',
            'title', 'description', 'content', 'content_json', 'block_note_content',
            'document_type', 'editor_type', 'is_public',
            'allow_comments', 'allow_sharing', 'allow_editing',
            'word_count', 'read_time', 'status', 'tags', 'comment_count',
            'created_at', 'updated_at', 'soft_delete'
        ]
        read_only_fields = ['id', 'author', 'word_count', 'read_time', 'created_at', 'updated_at']


class DocumentDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'author', 'author_username', 'title', 'description',
            'content', 'document_type', 'editor_type', 'is_public',
            'allow_comments', 'allow_sharing', 'allow_editing', 'status',
            'tags', 'comments', 'created_at', 'updated_at'
        ]

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value.strip()

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty")
        return value

    def validate_tags(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Tags must be a list")
        return value

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance

