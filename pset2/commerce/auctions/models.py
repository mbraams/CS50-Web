from django.contrib.auth.models import AbstractUser
from django.db import models


Categories = [
    ('a', 'Other'), 
    ('b', 'Electronics'),
    ('c', 'Home'),
    ('d', 'Sports'),
    ('e','Toys'),
    ('f', 'Clothes')]

class User(AbstractUser):
    def __str__(self):
        return self.username
    

class Bid(models.Model):
    bid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"${self.bid} by {self.user}"

class Comment(models.Model):
    comment = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True)



class Listing(models.Model):
    name = models.CharField("name", max_length=200)
    description = models.TextField("Description")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=1, choices=Categories, default='Other')
    image = models.ImageField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    bid = models.ManyToManyField(Bid, blank=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.name} is being listed by {self.owner}."


class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} has this listing on their watchlist: {self.listing}"