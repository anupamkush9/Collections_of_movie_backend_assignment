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
from rest_framework.decorators import api_view, throttle_classes

# class PostListView(PermissionRequiredMixin, ListView):
#     permission_required = "blog.view_post"
#     template_name = "blog/post_list.html"
#     model = Post


from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

class ExampleView(APIView):
    throttle_classes = [UserRateThrottle]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)


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
        