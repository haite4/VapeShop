from django.urls import path
from . import views


app_name = "blog"

urlpatterns = [
    path("blog/", views.show_blog, name="show-blog"),
    path("show-detail/<slug:slug_blog>/",views.show_detail, name="show-detail"),
    path("search_blog/", views.search_blog,name="search-blog")
]