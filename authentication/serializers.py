from django.db import transaction
from rest_framework import serializers

from authentication.models import User, UserType
from helpers.email_sender.vio_email_verification import vio_email_verify
from helpers.email_sender.volunteer_email_verification import volunteer_email_verify
from helpers.token_generators import gen_email_token


def email_choose(user_type, data):
    if user_type == UserType.VOLUNTEER:
        volunteer_email_verify(data['email'], data)

    if user_type == UserType.VIO:
        vio_email_verify(data['email'], data)

    if user_type == UserType.ADMIN:
        raise NotImplementedError("Admin email sending not implemented yet")


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True
    )

    email = serializers.EmailField(
        max_length=128, min_length=5
    )

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email', 'Email already in use'})

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data, user_type):
        validated_data['email_token'] = gen_email_token()

        data = {
            "email": validated_data['email'],
            "email_verify_link": f"https://localhost/api/auth/verify_email/{validated_data['email_token']}"
        }

        email_choose(user_type, data)
        user = User.objects.create_user(validated_data['email'],
                                        user_type,
                                        validated_data['password'],
                                        validated_data['email_token'])

        return user


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'token', 'user_type', 'state')

        read_only_fields = ['token']
