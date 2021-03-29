from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.forms import ModelForm

from .models import *

class NewListing(ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'description', 'category', 'image', 'price']

class NewBid(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

class NewComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":
        listing = NewListing(request.POST)
        if listing.is_valid():
            form = listing.cleaned_data
            title = form["name"]
            description = form["description"]
            image = form["image"]    
            category = form["category"]
            price = form["price"]
            user = User.objects.get(username=request.user)
            #add into sql database
            f = Listing(description = description, name = title, image = image, category = category, owner=user, price=price)
            f.save()            
            return HttpResponseRedirect('/')
        else:
            return render(request, "auctions/create.html",{
                "form" : listing})
    else:
        form = NewListing()
        return render(request, "auctions/create.html",{
            "form" : form
        })

@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    print(listing.image)
    watchlist =  Watchlist.objects.filter(user=request.user)              
    bid = NewBid()  
    comment = NewComment()
    if request.method == 'POST':
        message = ""
        if request.POST.get("button") == 'watchlist':
            if not watchlist.filter(listing=listing):
                Watchlist(listing = listing, user = request.user).save()
                message = "Added to watchlist!"
            else:
                watchlist.filter(listing=listing).delete()
                message = "Removed from watchlist!"

        #auction gets closed by owner    
        elif (request.POST.get("button") == "close"):
            listing.closed = True
            listing.save()
            message = "Listing closed!"

        #user commits a comment
        elif "comment" in request.POST:
            commentform = NewComment(request.POST)
            if commentform.is_valid():
                cleanedcomment = commentform.cleaned_data
                comment = cleanedcomment["comment"]
                newcomment = Comment(user=request.user, comment=comment)
                newcomment.save()

                #add comment to listing
                listing.comments.add(newcomment)
                listing.save()
                message = "comment submitted!"
                
                #create new form for additional comments
                comment = NewComment()
                
            else:
                comment = commentform
                message = "Error submitting your comment"

        #else its a bid
        else:
            bid = NewBid(request.POST)
            if bid.is_valid():
                form = bid.cleaned_data
                price = form["bid"]
                if price > listing.price:
                    newbid = Bid(bid = price, user = User.objects.get(username=request.user))
                    #save as bid
                    newbid.save()
                    #connect bid to the listing
                    listing.bid.add(newbid)
                    #update price with new (higher) bid
                    listing.price = price
                    listing.save()
                    return HttpResponseRedirect("/")
                #bid isnt high enough
                else:
                    message = "Amount not sufficient" 

        return render (request, "auctions/listing.html",{
            "listing" : listing, 
            "bid" : bid,
            "watchlist" : watchlist,
            "message" : message,
            "commentform" : comment
        })

    else:
         
        return render (request, "auctions/listing.html",{
            "listing" : listing, 
            "bid" : bid,
            "watchlist" : watchlist,
            "commentform" : comment
        })

@login_required
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    return render (request, "auctions/watchlist.html", {
        "watchlist" : watchlist
    })

def categories(request):
    
    return render(request, "auctions/categories.html", {
        "categories" : Categories
    })

def category_list(request, cat):
    categories = dict(Categories)
    category = categories.get(cat)
    listings = Listing.objects.filter(category=cat)
    return render(request, "auctions/category.html",{
        "category" : category,
        "listings" : listings
    })

def closedpages(request):
    print("now in closed")
    listings = Listing.objects.filter(closed=True)
    return render(request, "auctions/closed.html", {
        "listings" : listings
    })
