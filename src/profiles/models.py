from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse
from .utils import get_random_code
from django.db.models import QuerySet, Q
from posts.models import Post


class ProfileManager(models.Manager):

    # Get all the profiles that are available to invite for the
    # current logged in user.
    def profiles_available_to_invite(self, user):
        logged_in_user_profile = Profile.objects.get(user=user)
        friends = [Profile.objects.get(user=i) for i in list(logged_in_user_profile.friends.all())]
        pending_invitations_senders = [pending_invitation.sender for pending_invitation in
                                       Relationship.objects.filter(receiver=logged_in_user_profile)]
        pending_invitations_receivers = [pending_invitation.receiver for pending_invitation in
                                         Relationship.objects.filter(sender=logged_in_user_profile)]
        pending_invitation_profiles = pending_invitations_senders
        pending_invitation_profiles.extend(pending_invitations_receivers)
        profiles_to_be_excluded = []
        profiles_to_be_excluded.extend(pending_invitation_profiles)
        profiles_to_be_excluded.extend(friends)
        profiles_to_be_excluded.append(logged_in_user_profile)
        available_profiles = [profile for profile in list(Profile.objects.all())
                              if profile not in profiles_to_be_excluded]
        return available_profiles


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    gender_options = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=7, choices=gender_options, blank=True)
    country = models.CharField(max_length=70, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    # Function to return a list of friends.
    def get_friends(self):
        return self.friends.all()

    # Function to get total number of friends.
    def get_friends_count(self):
        return self.friends.all().count()

    # Function to get the queryset of posts associated with the logged in user-profile.
    def get_posts(self):
        # Approach - 1
        # posts = Post.objects.filter(author=self.user)
        # return posts

        # Approach - 2 : 'post_set' can be used because we have a reverse relation in Post model.
        # return self.post_set.all()

        # Approach - 3 : 'posts' can be used directly instead of 'post_set' because we have mentioned
        # (..., related_name='posts') in the field containing reverse relation in the Post model.
        return self.posts.all()

    # Function to get the number of posts associated with the logged in user-profile.
    def get_posts_count(self):
        # Approaches mentioned in the above function 'get_posts()' can be used here as well.
        # Approach - 3
        return self.posts.all().count()

    def __str__(self):
        return str(self.user.username)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        to_slug = self.slug
        # Create a slug from first_name and last_name if they both exist, else create a slug from username.
        # If the profile with same first_name and last_name exists, then append a random unique ID
        # with the slug and then save in the database.
        if ((self.first_name != self.__initial_first_name) or
            (self.last_name != self.__initial_last_name) or
            (self.slug == "")):
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + ' ' + str(self.last_name))
                slug_exists = Profile.objects.filter(slug=to_slug).exists()
                while slug_exists:
                    to_slug = slugify(to_slug + ' ' + str(get_random_code()))
                    slug_exists = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

    # Function to get the absolute url of the profile.
    def get_absolute_url(self):
        return reverse("profile-detail-view", kwargs={'slug': self.slug})


# Model that extends models.Manager, which performs interface for database operations.
class RelationshipManager(models.Manager):

    def invitations_received(self, receiver):
        query_set = Relationship.objects.filter(receiver=receiver, status='sent')
        return query_set

    def invitations_sent(self, sender):
        query_set = Relationship.objects.filter(sender=sender, status='sent')
        return query_set


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status_choices = (
        ('sent', 'sent'),
        ('accepted', 'accepted'),
    )
    status = models.CharField(max_length=10, choices=status_choices)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return str(self.sender) + '-->' + str(self.receiver) + ':' + str(self.status)
