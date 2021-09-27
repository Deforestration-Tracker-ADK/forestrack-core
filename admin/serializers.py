from django.db import transaction
from rest_framework import serializers

from admin.helpers import create_admin
from admin.models import Admin
from authentication.models import User
from volunteer.models import Volunteer


class AdminRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, min_length=4, required=True)
    last_name = serializers.CharField(max_length=255, min_length=4, required=True)
    nic = serializers.CharField(max_length=12, min_length=10, required=True)
    email = serializers.EmailField(max_length=128, min_length=5, required=True)

    class Meta:
        model = Admin
        fields = (
            'first_name', 'last_name', 'nic', 'user')

    def validate(self, attrs):
        if Admin.objects.filter(nic=attrs['nic']).exists() or Volunteer.objects.filter(nic=attrs['nic']).exists():
            raise serializers.ValidationError({'nic', 'NIC already in use'})

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({'email': "Email already exist in system"})

        # nic regix validation

        return super().validate(attrs)

    @transaction.atomic()
    def create(self, validated_data):
        user = create_admin(validated_data["email"])
        validated_data['user'] = user

        admin = Admin.objects.create(**validated_data)
        return admin
