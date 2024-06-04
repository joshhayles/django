from django.urls import path
from .views import BlogListView, BlogDetailView

urlpatterns = [
    path("", BlogListView.as_view(), name="home"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    
        # this means all blog post entries will start with post/
        # and to represent each post entry, we can use the auto-incrementing primary key, which is represented as an integer, <int:pk>
        # as an example, this will make the URL pattern for our first post: post/1
        # this works because of the get_absolute_url method we wrote in our Post model
]