from django.shortcuts import render
from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from blog.models import Post
from django.views import View
from rest_framework.views  import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
# class PostListView(PermissionRequiredMixin, ListView):
#     permission_required = "blog.view_post"
#     template_name = "blog/post_list.html"
#     model = Post
    
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    
# ref : https://testdriven.io/blog/django-permissions/
# ref : https://testdriven.io/blog/django-permissions/

class PermissionTestingView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    def get(self, request):
        print("request.user::::::::::",request.user)
        if not request.user.has_perm("blog.set_published_status"):
            return Response({"error":"You don't have permission to access it"})
        return Response({"Success":"API is working fine. Welcome...."})
        