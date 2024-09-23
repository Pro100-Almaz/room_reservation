from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, generics

from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny


class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class UserViewSet(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]