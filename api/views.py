from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from .serializers import *
from .models import *
from .permissions import IsSuperUser


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUser)  # expects a set of classes


class GuestView(generics.ListCreateAPIView):
    """Create (POST) and list (GET) all Guests on this URL. No need to create different endpoint
    for create since permission is same in this case (doesn't require super user)"""
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def perform_create(self, serializer):
        """Create new Guest on POST to linked URL. Owner must be passed
           in as a parameter since it was defined as a custom serializer attribute
           in serializers.py (permissions and interactions will be empty initially."""
        serializer.save(created_by=self.request.user)


class GuestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View extra details on each guest (GET). DELETE and PUT to delete and update record."""
    queryset = Guest.objects.all()
    serializer_class = GuestDetailSerializer

