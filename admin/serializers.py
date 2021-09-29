from django.db import transaction
from rest_framework import serializers

from admin.helpers import create_admin
from admin.models import SystemAdmin
from authentication.models import User
from volunteer.models import Volunteer


class AdminRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, min_length=4, required=True)
    last_name = serializers.CharField(max_length=255, min_length=4, required=True)
    nic = serializers.CharField(max_length=12, min_length=10, required=True)
    email = serializers.EmailField(max_length=128, min_length=5, required=True)

    class Meta:
        model = SystemAdmin
        fields = (
            'email', 'first_name', 'last_name', 'nic')

    def validate(self, attrs):
        if SystemAdmin.objects.filter(nic=attrs['nic']).exists() or Volunteer.objects.filter(nic=attrs['nic']).exists():
            raise serializers.ValidationError({'message', 'NIC already in use'})

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({'message': "Email already exist in system"})

        # nic regix validation

        return super().validate(attrs)

    @transaction.atomic()
    def create(self, validated_data):
        admin = create_admin(
            validated_data["email"],
            validated_data["first_name"],
            validated_data["last_name"],
            validated_data["nic"]
        )

        return admin
