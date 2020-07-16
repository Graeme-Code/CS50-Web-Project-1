from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # I'm gonna create a path to an entry
    path("<str:entry>", views.entry, name = "entry"),
    #create a pth to search results I alomst want to say after the ? take the value of q.
    path("search/", views.search, name ="search_result"),
    #create path to new page
    path("newpage/", views.newpage, name = "newpage"),
    path("editpage/<str:title>", views.editpage, name="editpage"),
    path("randompage/", views.randompage, name="randompage")
]
