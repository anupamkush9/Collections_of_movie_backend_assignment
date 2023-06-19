# views.py
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse
from accounts.models import RequestCounter
from rest_framework.decorators import api_view, authentication_classes, permission_classes

@api_view(['GET'])
@authentication_classes([TokenAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def reset_request_count(request):
    RequestCounter.objects.update(count=0)
    return JsonResponse({'message': 'Request count reset successfully'})

@api_view(['GET'])
@authentication_classes([TokenAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_request_count(request):
    request_counter = RequestCounter.objects.first()
    if request_counter:
        return JsonResponse({'requests': request_counter.count})
    else:
        return JsonResponse({'requests': 0})


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        if User.objects.filter(username=username).exists():
            user = User.objects.filter(username=username).first()
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token)}, status=201)
        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)

        return Response({'access_token': str(refresh.access_token)}, status=201)
