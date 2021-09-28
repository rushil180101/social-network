from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Relationship


# Django signal to create a profile instance as soon as a new user is registered.
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    # Other operations instead of 'created' can be 'modified', 'deleted'.
    if created:
        Profile.objects.create(user=instance)


# Signal to add friends in the friends list of both the sender and receiver once the status
# of the relationship if 'accepted'.
@receiver(post_save, sender=Relationship)
def post_save_add_friends(sender, instance, created, **kwargs):
    s = instance.sender
    r = instance.receiver
    if instance.status == 'accepted':
        # 'friends' is a many-to-many field and more pointers (foreign keys) can be added to this list
        # using the add() function as follows.
        s.friends.add(r.user)
        r.friends.add(s.user)
        s.save()
        r.save()
