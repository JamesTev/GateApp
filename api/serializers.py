from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class GuestSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance to JSON format. The ModelSerializer class simply provides a
       shortcut compared to the normal Serializer implementation by automatically declaring fields that
       match the corresponding model definition. It also provides basic default .create() and .update()
       methods and provides some basic validation. See http://www.django-rest-framework.org/api-guide/serializers/"""

    created_by = serializers.ReadOnlyField(source='created_by.username')
    gate_interactions = serializers.PrimaryKeyRelatedField(many=True, queryset=GateActivity.objects.all())
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=GuestPermission.objects.all())
    # custom override of this attribute - we need to specify that the serialized representation of the owner
    # field is just that owner's username

    class Meta:
        """Meta class to map serializer's fields to model fields."""
        model = Guest
        # can exclude any fields below that shouldn't be displayed by API
        fields = ('id', 'first_name', 'surname', 'created_by', 'created_on', 'gate_interactions', 'permissions')
        read_only_fields = ('created_on', 'created_by')

    # can override more methods like validate() to add further validation or serialization
    # functionality


class UserSerializer(serializers.ModelSerializer):

    created_guests = serializers.PrimaryKeyRelatedField(many=True, queryset=Guest.objects.all())
    permissions_granted = serializers.PrimaryKeyRelatedField(many=True, queryset=GuestPermission.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'created_guests', 'permissions_granted')

