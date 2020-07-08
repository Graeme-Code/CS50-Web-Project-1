from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # I'm gonna create a path to an entry
    path("<str:entry>", views.entry, name = "entry")
]
