from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),    
    path("create", views.create, name="create"),
    path("random", views.randompage, name="random"),   
    path("edit/<str:name>", views.editpage, name="edit"),
    path("?q=<str:name>", views.search, name="search"),
    path("<str:name>", views.page, name="entry")
    
]
