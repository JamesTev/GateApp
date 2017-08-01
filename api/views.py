from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, CreateUserSerializer
from .models import *
from .permissions import IsSuperUser


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUser)  # expects a set of classes

    def perform_create(self, serializer):
        """Save the POST data to create new User. Owner must be passed
           in as a parameter since it was defined as a custom serializer attribute
           in serializers.py"""
        serializer.save()

