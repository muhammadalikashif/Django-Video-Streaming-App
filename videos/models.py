from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from video_project import settings

class Video(models.Model):
    title = models.CharField(max_length=200)
    publisher = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    age_rating = models.CharField(max_length=10)
    video_file = models.FileField(upload_to='videos/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)


from django.conf import settings

class CommentRating(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.text:
            return f"Comment by {self.user.username}: {self.text[:50]}..."
        elif self.rating:
            return f"Rating by {self.user.username}: {self.rating}/5"
        else:
            return f"Empty entry by {self.user.username}"