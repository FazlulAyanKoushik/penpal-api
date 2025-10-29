from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save

from accounts.signals import post_save_user_profile

User = get_user_model()

# Using Django's default User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    preferences = models.JSONField(blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        db_table = "profiles"


post_save.connect(post_save_user_profile, sender=User)
