# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TagViewSet,
    DocumentListCreateView,
    DocumentRetrieveUpdateDestroyView,
    CommentListCreateView,
    CommentRetrieveUpdateDestroyView
)


router = DefaultRouter()
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', DocumentListCreateView.as_view(), name='document-list-create'),
    path('docs/<str:pk>/', DocumentRetrieveUpdateDestroyView.as_view(), name='document-retrieve-update-destroy'),

    path('docs/<str:document_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('docs/comments/<str:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-retrieve-update-destroy'),
]