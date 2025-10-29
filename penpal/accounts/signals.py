
def post_save_user_profile(sender, instance, created, **kwargs):
    from accounts.models import Profile

    if created:
        Profile.objects.create(user=instance)