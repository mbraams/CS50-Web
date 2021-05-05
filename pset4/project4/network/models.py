from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class User(AbstractUser):
    def __str__(self):
        return self.username

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ForeignKey(Like, on_delete=models.CASCADE)

class Post(models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ForeignKey(Like, on_delete=models.CASCADE)
    reactions = models.ForeignKey(Reaction, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

