from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("random", views.random, name="random"),
    path("edit/<str:entryName>", views.edit, name="edit"),
    path("wiki/<str:entryName>", views.entry, name="entry"),
    path("<str:entryName>", views.entry, name="entry"),        
]
