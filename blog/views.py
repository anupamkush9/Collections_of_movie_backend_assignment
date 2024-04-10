from django.shortcuts import render
from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from blog.models import Post

# class PostListView(PermissionRequiredMixin, ListView):
#     permission_required = "blog.view_post"
#     template_name = "blog/post_list.html"
#     model = Post
    
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'