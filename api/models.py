from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Guest(models.Model):
    """This class represents the guests model which holds information pertaining to the
    guests that have been granted access to the gateApp, as well as the user responsible
    for their creation etc."""
    first_name = models.CharField(max_length=255, blank=False)
    surname = models.CharField(max_length=255, blank=False)
    email = models.EmailField()
    mobile = models.CharField(max_length=30, unique=True)
    created_by = models.ForeignKey('auth.User', related_name='created_guests', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of model instance"""
        return "{0} {1}".format(self.first_name, self.surname)


class GateActivity(models.Model):
    """This model is used to log all interactions with the gate, especially the entity responsible
    for operating the gate at a certain date/time"""
    date = models.DateTimeField(auto_now_add=True)
    responsible_user = models.ForeignKey('auth.User', related_name='gate_interactions', on_delete=models.CASCADE, null=True, blank=True)
    responsible_guest = models.ForeignKey('Guest', related_name='gate_interactions', on_delete=models.CASCADE, null=True, blank=True)
    gate_status = models.PositiveSmallIntegerField(choices=((1, 'HIGH'), (0, 'LOW')))

    def __str__(self):
        if self.responsible_user:
            return "Interaction by {0} @ {1}".format(self.responsible_user.username, self.date)
        elif self.responsible_guest:
            return "Interaction by {0} {1} @ {2}".format(self.responsible_guest.first_name, self.responsible_guest.surname, self.date)


class GuestPermission(models.Model):
    """This model is used to log all guest permissions in order perform authentication based on creation and
    expiry dates."""
    token = models.CharField(max_length=50, unique=True)
    guest = models.ForeignKey('Guest', related_name='permissions', on_delete=models.CASCADE)
    granted_by = models.ForeignKey('auth.User', related_name='permissions_granted', on_delete=models.CASCADE)
    granted_on = models.DateField(auto_now_add=True)
    starts_on = models.DateTimeField(default=timezone.now)
    expires_on = models.DateTimeField()
    once_off = models.BooleanField(default=False)
    once_off_used = models.BooleanField(default=False)

    def __str__(self):
        return "Permission for {0} granted by {1}. Expires on {2}".format(self.guest.first_name, self.granted_by.username, self.expires_on)




