from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey, ManyToManyField

defaultuser = 1

class User(AbstractUser):
    def __str__(self):
        return self.username

class Follow(models.Model):
    followedUser = ForeignKey(User, on_delete=CASCADE, related_name="followingUser", default=defaultuser)
    followingUser = ForeignKey(User, on_delete=CASCADE, related_name="followedUser", default=defaultuser)    

class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    reply = models.CharField(max_length=250, default="")
    def __str__(self):
        return f"{self.user} replied {self.reply}."

class Post(models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reactions = models.ManyToManyField(Reaction, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likecount = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user} posted: {self.content}, at {self.timestamp}"
    def serialize(self):
        return {
            "content": self.content,
            "user": self.user.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "id" : self.id,
            "likes" : self.likes
        }

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user} liked {self.post}"
    def serialize(self):
        return{
            "user" : self.user,
            "id" : self.id
        }
