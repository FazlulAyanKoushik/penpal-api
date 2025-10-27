# serializers.py
from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    tags = serializers.JSONField()
    block_note_content = serializers.JSONField()

    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'description',
            'content',
            'block_note_content',
            'document_type',
            'editor_type',
            'status',
            'author',
            'author_name',
            'created_at',
            'updated_at',
            'word_count',
            'read_time',
            'tags',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'author_name']

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