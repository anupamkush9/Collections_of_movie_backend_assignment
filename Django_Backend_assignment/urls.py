"""Django_Backend_assignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
import movies_collection.views
from accounts.views import get_request_count, reset_request_count
from rest_framework_simplejwt import views as jwt_views
from blog.views import PostListView, PermissionTestingView
from django.contrib.auth import views as auth_views

router_v1 = routers.DefaultRouter()
router_v1.register(r"movies", movies_collection.views.MovieViewSet)
router_v1.register(r"collection", movies_collection.views.CollectionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # path('collections/', include('movies_collection.urls')),
    path("api/v1/", include(router_v1.urls), name="api-root"),
    # path('request-count/', get_request_count),
    path('request-count/', get_request_count, name='get_request_count'),
    path('request-count/reset/', reset_request_count, name='reset_request_count'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('perm_testing_view/', PermissionTestingView.as_view(), name='permission-testing-view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]


