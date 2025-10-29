import uuid
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AuditLog(models.Model):
    """
    Generic audit trail entry for tracking user/system actions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        help_text="User who performed the action (if available)."
    )

    # Action type
    verb = models.CharField(
        max_length=50,
        choices=[
            ('create', 'Create'),
            ('update', 'Update'),
            ('delete', 'Delete'),
            ('publish', 'Publish'),
            ('login', 'Login'),
            ('logout', 'Logout'),
            ('restore', 'Restore'),
            ('other', 'Other'),
        ],
        help_text="Type of action performed."
    )

    # Generic target object (any model)
    target_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        help_text="Django ContentType of the affected object."
    )
    target_id = models.CharField(max_length=64, help_text="Primary key of the affected object.")
    diff = models.JSONField(default=dict, blank=True, help_text="Changed fields (before/after snapshot).")

    # Request context
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, help_text="User agent string from the request.")

    # Metadata
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['actor']),
            models.Index(fields=['verb']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['target_type', 'target_id']),
        ]
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        actor_name = self.actor.username if self.actor else "System"
        return f"[{self.verb.upper()}] {actor_name} → {self.target_type}({self.target_id})"

    @property
    def target_object(self):
        """
        Return the related target object instance (if exists).
        """
        if not self.target_type:
            return None
        model_class = self.target_type.model_class()
        try:
            return model_class.objects.filter(pk=self.target_id).first()
        except Exception:
            return None
