from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication
from django.utils.crypto import get_random_string
from .serializers import *
from .models import *
from .permissions import IsSuperUser


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('first_name', 'username', 'last_name')
    permission_classes = (permissions.IsAuthenticated, )  # expects a set of classes


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
    permission_classes = (permissions.IsAuthenticated,)  # needs to have user logged in to associate responsible user with new guest
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

    def delete(self, request, *args, **kwargs):
        """Override delete method to only allow superuser to delete guest records."""
        if request.user.is_superuser:
            return self.destroy(request, *args, **kwargs)
        else:
            raise exceptions.PermissionDenied


class GuestPermissionView(generics.ListCreateAPIView):
    """Create (POST) and list (GET) all granted guest permissions. No need to create different endpoint
    for create since permission is same in this case (doesn't require super user)"""
    queryset = GuestPermission.objects.all()
    serializer_class = GuestPermissionSerializer

    def perform_create(self, serializer):
        """Create new Guest on POST to linked URL. Owner must be passed
           in as a parameter since it was defined as a custom serializer attribute
           in serializers.py (permissions and interactions will be empty initially."""
        serializer.save(granted_by=self.request.user, token=get_random_string(length=16))


class GuestPermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View extra details on each guest (GET). DELETE and PUT to delete and update record."""
    queryset = GuestPermission.objects.all()
    serializer_class = GuestPermissionSerializer


class GateInteractionView(generics.ListAPIView):
    """Allows GET to appropriate endpoint to list all gate interactions"""
    queryset = GateActivity.objects.all()
    serializer_class = GateActivitySerializer


class UserGateInteractionView(generics.ListCreateAPIView):
    """Only allows POST to appropriate endpoint with supplied token to create USER ('staff')
    gate interaction record (ie for staff user to operate gate). GET only returns
    user (not guest) interactions."""
    queryset = GateActivity.objects.filter(responsible_user__isnull=False)
    serializer_class = UserGateActivitySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        # override this method in order to explicitly set the responsible user
        serializer.save(responsible_user=self.request.user)


class GuestGateInteractionView(generics.ListCreateAPIView):
    """POST to appropriate endpoint with supplied token to create GUEST
    gate interaction record (ie for guest to operate gate). GET only returns
    guest interactions."""
    queryset = GateActivity.objects.filter(responsible_guest__isnull=False)  # only guest interactions
    serializer_class = GuestGateActivitySerializer
    permission = None

    def perform_create(self, serializer):

        try:
            self.permission = GuestPermission.objects.get(token=self.request.POST['token'])
        except KeyError:
            raise serializers.ValidationError(detail={'error detail': 'No permission token supplied'})
        except GuestPermission.DoesNotExist:
            raise serializers.ValidationError(detail={'error detail': 'Invalid permission token'})

        resp_guest = self.permission.guest  # extract resp guest from permission
        if resp_guest and self.check_permission():
            serializer.save(responsible_guest=resp_guest)

    def check_permission(self):

        if timezone.now() > self.permission.expires_on:
            raise exceptions.PermissionDenied(detail={"error detail": "Permission expired on {0}".format(self.permission.expires_on)})
        elif timezone.now() < self.permission.starts_on:
            raise exceptions.PermissionDenied(
                detail={'error detail': "Permission not yet active. Activation begins {0}".format(self.permission.expires_on)})
        elif self.permission.once_off and self.permission.once_off_used:
            raise exceptions.PermissionDenied(detail={'error detail': 'Once off permission already used'})
        else:
            # valid permission if this point is reached
            if self.permission.once_off:
                self.permission.once_off_used = True
                self.permission.save()  # update permission record
            return True
