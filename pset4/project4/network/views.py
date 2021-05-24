from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Post
import json
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt


class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

def index(request):
    newpost = NewPost()
    posts = Post.objects.all().order_by('-timestamp')

    return render(request, "network/index.html", {
        "newpost" : newpost, "posts" : posts
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
def newposts(request):
     #this is for composing posts
    if request.method == "POST":
        print("in newpost")
        data = json.loads(request.body)
        owner = request.user
        message = data.get("body", "")
        post = Post(content=message, user=owner)
        post.save()
        return JsonResponse({"message": "Post sent succesfully."}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)

def allposts(request):
    posts = Post.objects.all().order_by('-timestamp')
    return JsonResponse([posts.serialize() for post in posts], safe=False)
    



        
