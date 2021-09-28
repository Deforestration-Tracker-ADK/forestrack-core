from datetime import date

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
    dob = serializers.DateField(required=True)
    district = serializers.CharField(max_length=255, min_length=4, required=True)
    address = serializers.CharField(max_length=255, min_length=4, required=True)
    specialConditions = serializers.CharField(max_length=255, min_length=4)
    preferredLanguage = EnumChoiceField(Language)
    highestEducation = EnumChoiceField(HighestEducation)
    contactNumber = serializers.CharField(max_length=15, min_length=9, required=True)
    user = UserRegisterSerializer()

    class Meta:
        model = Volunteer
        fields = (
            'first_name', 'last_name', 'nic', 'nameNIC', 'gender', 'district', 'address', 'specialConditions',
            'preferredLanguage', 'highestEducation', 'contactNumber', 'user', "dob")

    def validate(self, attrs):
        if attrs['registrationDate'] >= date.today():
            raise serializers.ValidationError({"message": "The registration day must be in the past"})

        # check  if above 18
        if Volunteer.objects.filter(nic=attrs['nic']).exists():
            raise serializers.ValidationError({'message', 'NIC already in use'})

        if not 12 >= len(attrs["contactNumber"]) >= 9:
            raise serializers.ValidationError({"message": "The contact number must be within 12 to 9 digits"})
        # add nic regex validation

        return super().validate(attrs)

    @transaction.atomic()
    def create(self, validated_data):
        user = UserRegisterSerializer().create(validated_data['user'], UserType.VOLUNTEER)
        validated_data['user'] = user

        volunteer = Volunteer.objects.create(**validated_data)
        return volunteer
