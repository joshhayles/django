from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post

class BlogListView(ListView):
    model = Post 
    template_name = "home.html"

class BlogDetailView(DetailView):
    model = Post 
    template_name = "post_detail.html"

class BlogCreateView(CreateView):
    model = Post
    template_name = "post_new.html"
    fields = ["title", "author", "body"]

class BlogUpdateView(UpdateView):
    model = Post 
    template_name = "post_edit.html"
    fields = ["title", "body"]

class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home") # will redirect the user to the homepage

    # reverse_lazy will "delay" the actual call to the URLConf until the moment it is needed vs when our BlogDeleteView is being evaluated
    
    # the moment BlodDeleteView is called, 'reverse' (which is the other option vs reverse_lazy) needs to have the information from the URLConf to find the proper route for the URL name "home." However, it may not have that information in time for the success_url.