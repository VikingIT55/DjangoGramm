from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=75)
    images = models.ImageField(upload_to='post_images')
    tags = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.tags = ''.join([tag if tag.startswith('#') else '#' + tag for tag in self.tags.split()])
        super(Post, self).save(*args, **kwargs)
