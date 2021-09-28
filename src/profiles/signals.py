from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


# Django signal to create a profile instance as soon as a new user is registered.
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    # Other operations instead of 'created' can be 'modified', 'deleted'.
    if created:
        Profile.objects.create(user=instance)
