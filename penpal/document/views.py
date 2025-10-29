# views.py
from django.db.models import Q
from django.template.context_processors import request
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Document, Tag, Comment
from .permissions import DocumentPermission, CommentPermission
from .serilaizers import TagSerializer, CommentSerializer, DocumentListSerializer, DocumentDetailSerializer, \
    DocumentSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['document_type', 'status', 'editor_type', 'is_public', 'author__id']
    search_fields = ['title', 'description', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DocumentSerializer
        return DocumentListSerializer

    def get_queryset(self):
        user = self.request.user
        qs = (Document.objects.select_related('author')
              .prefetch_related('tags','comments')
              .filter(soft_delete=False))
        if user.is_authenticated:
            qs = qs.filter(Q(is_public=True) | Q(author=user))
        else:
            qs = qs.filter(is_public=True)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DocumentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a document.
    """
    serializer_class = DocumentDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, DocumentPermission]
    queryset = (Document.objects.select_related('author')
                .prefetch_related('tags','comments')
                .filter(soft_delete=False))

    def perform_destroy(self, instance):
        # Soft delete instead of actual delete
        instance.soft_delete = True
        instance.save()


class CommentListCreateView(generics.ListCreateAPIView):
    """
    List all comments for a document or create a new one.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CommentPermission]

    def get_queryset(self):
        document_id = self.kwargs.get('document_id')
        return (Comment.objects.select_related('document', 'author')
                .filter(document_id=document_id, soft_delete=False))

    def perform_create(self, serializer):
        document_id = self.kwargs.get('document_id')
        serializer.save(author=self.request.user, document_id=document_id)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CommentPermission]
    queryset = (Comment.objects.select_related('document', 'author')
                .filter(soft_delete=False))

    def perform_destroy(self, instance):
        instance.soft_delete = True
        instance.save()