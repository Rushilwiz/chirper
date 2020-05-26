from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author}'s post on {self.date_posted}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
