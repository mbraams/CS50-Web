from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.views.decorators import csrf
from .models import Like, User, Post
import json
from django.http import JsonResponse
from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_exempt


class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

def index(request):
    newpost = NewPost()
    userLikes = Like.objects.filter(user=request.user)
    likedposts = []
    for like in userLikes:
        likedposts.append(like.post.id)
    posts = Post.objects.all().order_by('-timestamp')
    #paginate amount of posts per page
    p = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)


    return render(request, "network/index.html", {
        "newpost" : newpost, "page_obj" : page_obj, "likedposts" : likedposts
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
    
    return JsonResponse([post.serialize() for post in posts], safe=False)
    
@csrf_exempt
def getlikes(request, post_id): 
    likesOnPost = Like.objects.filter(post=post_id, user=request.user)
    found = {'liked' : False}
    if request.method == "GET":
        if likesOnPost:
            found['liked'] = True
        return JsonResponse(found)
    #liked/unliked
    else:
        if request.method == "POST":    
            post = Post.objects.get(id=post_id)        
            data = json.loads(request.body)
            liked = data.get("like")
            print(liked)
            if liked:                
                newlike = Like(user=request.user, post=post)
                newlike.save()
                message = "post liked"
            else:
                likesOnPost.delete()            
                message = "like deleted"
            post.likecount = Like.objects.filter(post=post_id).count()
            print(post.likecount)
            post.save()
            return JsonResponse({"message": message}, status=201)

@csrf_exempt
@login_required
def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
            post.save()
            return JsonResponse({"message": "Post editted"}, status=201)
    else:
        return JsonResponse({"error":"error, method has to be 'PUT'"})

def viewprofile(request, user_id):
    profile = User.objects.get(id=user_id)
    posts = Post.objects.filter(user=user_id).order_by('-timestamp')
    followers = profile.followers.count()
    follows = profile.follows.count()

    userLikes = Like.objects.filter(user=request.user)
    likedposts = []
    for like in userLikes:
        likedposts.append(like.post.id)
    #paginate amount of posts per page
    p = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    context = {
        "profile" : profile,
        "posts" : page_obj,
        "followers" : followers,
        "follows": follows,
        "likedposts" : likedposts
       }

    return render(request, "network/profile.html", context)

def getfollow(request, profile_id):
    follows = User.objects.filter(id=request.user, follows=profile_id)
    found = {'liked' : False}
    #checking if user is already following or not
    if request.method == "GET":
        if follows:
            found['liked'] = True
        return JsonResponse(found)
    #user following/unfollowing profile

    #change this still
    else:
        if request.method == "POST":    
            post = Post.objects.get(id=post_id)        
            data = json.loads(request.body)
            liked = data.get("like")
            print(liked)
            if liked:                
                newlike = Like(user=request.user, post=post)
                newlike.save()
                message = "post liked"
            else:
                likesOnPost.delete()            
                message = "like deleted"
            post.likecount = Like.objects.filter(post=post_id).count()
            print(post.likecount)
            post.save()
            return JsonResponse({"message": message}, status=201)





        
