from django.db import models
from django.core.validators import FileExtensionValidator


class Post(models.Model):
    author = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])],
        blank=True
    )
    content = models.TextField(blank=True)
    liked_by = models.ManyToManyField('profiles.Profile', blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content[:5] + '...') + str('(' + str(self.author) + ')')

    def likes(self):
        return self.liked_by.all().count()

    def num_of_comments(self):
        # Approach - 1
        # Comment.objects.filter(post=self.pk).count()

        # Approach - 2 (model_set.all())
        return self.comment_set.all().count()

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment - ' + str(self.body[:10] + '...') + str('(' + str(self.user) + ')')


class Like(models.Model):
    user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    like_unlike_options = (
        ('Like', 'Like'),
        ('Unlike', 'Unlike'),
    )
    like_unlike_value = models.CharField(max_length=8, choices=like_unlike_options, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.like_unlike_value) + ' | ' + str(self.user) + ' --> ' + str(self.post)
