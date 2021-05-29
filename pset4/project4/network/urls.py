
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newposts, name="newpost"),
    path("allposts", views.allposts, name="allposts"),
    path("like/<int:post_id>", views.getlikes, name="like"),
    path("edit/<int:post_id>", views.edit, name="edit")
]
