from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Guest, GateActivity, GuestPermission


class GuestPermissionSerializer(serializers.ModelSerializer):
    granted_by = serializers.ReadOnlyField(source='granted_by.username')

    class Meta:
        """Meta class to map serializer's fields to model fields."""
        model = GuestPermission
        # can exclude any fields below that shouldn't be displayed by API
        fields = ('id', 'guest', 'token', 'granted_by', 'granted_on', 'expires_on', 'once_off', 'once_off_used')
        read_only_fields = ('created_on', 'created_by', 'token')


class GuestSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance to JSON format. The ModelSerializer class simply provides a
       shortcut compared to the normal Serializer implementation by automatically declaring fields that
       match the corresponding model definition. It also provides basic default .create() and .update()
       methods and provides some basic validation. See http://www.django-rest-framework.org/api-guide/serializers/"""

    created_by = serializers.ReadOnlyField(source='created_by.username')
    # custom override of this attribute - we need to specify that the serialized representation of the owner
    # field is just that owner's username

    class Meta:
        """Meta class to map serializer's fields to model fields."""
        model = Guest
        # can exclude any fields below that shouldn't be displayed by API
        fields = ('id', 'first_name', 'surname', 'created_by', 'email', 'mobile', 'created_on')
        read_only_fields = ('created_on', 'created_by')


class GuestDetailSerializer(GuestSerializer):
    """Detail serializer for individual guest instances. Indicates extra information such as the guest's
       gate interactions and permissions. Inherits from GuestSerializer to avoid redefining created_by"""
    gate_interactions = serializers.PrimaryKeyRelatedField(many=True, queryset=GateActivity.objects.all())
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=GuestPermission.objects.all())

    class Meta(GuestSerializer.Meta):
        """Inherit from GuestSerializer - only need to override fields attribute"""
        fields = ('id', 'first_name', 'surname', 'created_by', 'created_on', 'mobile', 'gate_interactions', 'permissions')


class UserSerializer(serializers.ModelSerializer):

    created_guests = serializers.PrimaryKeyRelatedField(many=True, queryset=Guest.objects.all())
    permissions_granted = serializers.PrimaryKeyRelatedField(many=True, queryset=GuestPermission.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'created_guests', 'permissions_granted')


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

    def create(self, validated_data):
        """Override create method to set password manually from serialized data (which contains hashed password)"""
        # same as super.create() which calls ModelSerializer.create() - python requires those
        # two explicit arguments in super() call
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



