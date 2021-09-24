from django.db import transaction
from enumchoicefield import ChoiceEnum, EnumChoiceField
from rest_framework import serializers

from authentication.models import UserType
from authentication.serializers import UserRegisterSerializer
from volunteer.models import Volunteer


class Gender(ChoiceEnum):
    MALE = "M",
    FEMALE = "F",
    UNSPECIFIED = "UN",


class Language(ChoiceEnum):
    SINHALA = 'S',
    ENGLISH = 'E',
    TAMIL = 'T',


class HighestEducation(ChoiceEnum):
    OL = 'OL',
    AL = 'AL',
    UNDERGRADUATE = 'UG',
    POSTGRADUATE = 'PG',


class VolunteerRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, min_length=4, required=True)
    last_name = serializers.CharField(max_length=255, min_length=4, required=True)
    nic = serializers.CharField(max_length=12, min_length=10, required=True)
    nameNIC = serializers.CharField(max_length=255, min_length=4, required=True)
    gender = EnumChoiceField(Gender)
    district = serializers.CharField(max_length=255, min_length=4, required=True)
    address = serializers.CharField(max_length=255, min_length=4, required=True)
    specialConditions = serializers.CharField(max_length=255, min_length=4)
    preferredLanguage = EnumChoiceField(Language)
    highestEducation = EnumChoiceField(HighestEducation)
    user = UserRegisterSerializer()

    class Meta:
        model = Volunteer
        fields = (
            'first_name', 'last_name', 'nic', 'nameNIC', 'gender', 'district', 'address', 'specialConditions',
            'preferredLanguage', 'highestEducation', 'user')

    def validate(self, attrs):
        if Volunteer.objects.filter(nic=attrs['nic']).exists():
            raise serializers.ValidationError({'nic', 'NIC already in use'})

        # add nic regex validation

        return super().validate(attrs)

    @transaction.atomic()
    def create(self, validated_data):
        user = UserRegisterSerializer().create(validated_data['user'], UserType.VOLUNTEER)
        validated_data['user'] = user

        volunteer = Volunteer.objects.create(**validated_data)
        return volunteer