from django.db import transaction
from rest_framework import serializers

from authentication.models import UserType
from authentication.serializers import UserRegisterSerializer
from vio.models import Vio


class VioRegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, min_length=4)
    description = serializers.CharField(max_length=255, min_length=4)
    registrationNo = serializers.CharField(max_length=12, min_length=10)
    address = serializers.CharField(max_length=255, min_length=4, required=True)
    district = serializers.CharField(max_length=255, min_length=4, required=True)
    user = UserRegisterSerializer()

    class Meta:
        model = Vio
        fields = ('name', 'description', 'registrationNo', 'user', 'address', 'district')

    def validate(self, attrs):
        if Vio.objects.filter(registrationNo=attrs['registrationNo']).exists():
            raise serializers.ValidationError({'registrationNo', 'The Registration Number is already in use'})

        return super().validate(attrs)

    @transaction.atomic()
    def create(self, validated_data):
        user = UserRegisterSerializer().create(validated_data['user'], UserType.VIO)
        validated_data['user'] = user

        vio = Vio.objects.create(**validated_data)
        return vio
