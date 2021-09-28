from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from .utils import get_random_code


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

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        # Create a slug from first_name and last_name if they both exist, else create a slug from username.
        # If the profile with same first_name and last_name exists, then append a random unique ID
        # with the slug and then save in the database.
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

    def __str__(self):
        return str(self.sender) + '-->' + str(self.receiver) + ':' + str(self.status)
