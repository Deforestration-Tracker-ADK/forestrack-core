import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from authentication.enums import UserState
from authentication.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        # print(auth_data, "auth data")
        auth_token = auth_data.split(" ")
        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed("Auth Token not valid")

        token = auth_token[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

            if payload["state"] == UserState.EMAIL_UNVERIFIED:
                raise exceptions.AuthenticationFailed("User must verify email")

            user = User.objects.get(id=payload["id"])
            return user, token

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token is expired, login again")

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Token is invalid")

        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed("No such user in system")
