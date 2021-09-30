from rest_framework import serializers

from admin.models import SystemAdmin
from volunteer.models import Volunteer


class AdminRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, min_length=4, required=True)
    last_name = serializers.CharField(max_length=255, min_length=4, required=True)
    nic = serializers.CharField(max_length=12, min_length=10, required=True)

    class Meta:
        model = SystemAdmin
        fields = (
            'first_name', 'last_name', 'nic')

    def validate(self, attrs):
        if SystemAdmin.objects.filter(nic=attrs['nic']).exists() or Volunteer.objects.filter(nic=attrs['nic']).exists():
            raise serializers.ValidationError({'message': 'NIC already in use'})

        # nic regix validation

        return super().validate(attrs)
