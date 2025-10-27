# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Document
from .serilaizers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()  # Add queryset for router
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['document_type', 'status', 'editor_type']
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['created_at', 'updated_at', 'title', 'word_count']
    ordering = ['-updated_at']

    def get_queryset(self):
        return Document.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get document statistics for the authenticated user"""
        queryset = self.get_queryset()

        stats = {
            'total': queryset.count(),
            'published': queryset.filter(status='published').count(),
            'draft': queryset.filter(status='draft').count(),
            'total_words': sum(doc.word_count for doc in queryset),
            'types': {},
            'editor_types': {}
        }

        # Document types
        for doc_type, _ in Document._meta.get_field('document_type').choices:
            stats['types'][doc_type] = queryset.filter(document_type=doc_type).count()

        # Editor types
        for editor_type, _ in Document._meta.get_field('editor_type').choices:
            stats['editor_types'][editor_type] = queryset.filter(editor_type=editor_type).count()

        return Response(stats)