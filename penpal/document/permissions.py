from rest_framework import permissions


# ----------------------------
# DOCUMENT-LEVEL PERMISSIONS
# ----------------------------
class DocumentPermission(permissions.BasePermission):
    """
    Document-level access control.

    - SAFE methods (GET, HEAD, OPTIONS): allowed if document is public OR user is owner
    - Write (PUT, PATCH, DELETE): allowed only for the document owner
    """

    def has_object_permission(self, request, view, obj):
        # SAFE (read-only) methods
        if request.method in permissions.SAFE_METHODS:
            return obj.is_public or obj.author == request.user

        # Write: only author can update/delete
        return obj.author == request.user


# ----------------------------
# COMMENT-LEVEL PERMISSIONS
# ----------------------------
class CommentPermission(permissions.BasePermission):
    """
    Comment-level permissions:
    - SAFE: allowed for public documents or document owner
    - Create: only authenticated users (handled by IsAuthenticated)
    - Update/Delete: only comment author or document owner
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.document.is_public or obj.document.author == request.user

        # Update or Delete
        return obj.author == request.user or obj.document.author == request.user


# ----------------------------
# MEDIA-ASSET PERMISSIONS
# ----------------------------
class MediaAssetPermission(permissions.BasePermission):
    """
    MediaAsset permissions:
    - SAFE: owner or document author can view
    - Modify: owner or document author can upload/delete
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.owner == request.user or obj.document.author == request.user

        # Write permissions
        return obj.owner == request.user or obj.document.author == request.user
