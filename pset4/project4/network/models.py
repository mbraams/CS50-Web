from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class User(AbstractUser):
    def __str__(self):
        return self.username

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user} liked this post."

class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Like)
    reply = models.CharField(max_length=250, default="")
    def __str__(self):
        return f"{self.user} replied {self.reply}."

class Post(models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Like, blank=True)
    reactions = models.ManyToManyField(Reaction, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} posted: {self.content}, at {self.timestamp}"
    def serialize(self):
        return {
            "content": self.content,
            "user": self.user,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

