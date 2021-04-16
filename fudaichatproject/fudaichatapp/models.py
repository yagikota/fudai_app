from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(null=True, blank=True, default=0)
    dislikes = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.content[:30]
