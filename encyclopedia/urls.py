from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry"),
    path("entry/random", views.random_entry, name="random_entry"),
    path("search/entry", views.search, name="search"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("entry/create", views.create_entry, name="create_entry")
]
