from django.contrib.auth import authenticate
from rest_framework import response, status
from rest_framework.generics import GenericAPIView

from authentication.enums import UserState
from authentication.models import UserType
from authentication.serializers import LoginSerializer
from authentication.services import AuthService
from vio.models import Vio
from volunteer.models import Volunteer


# Create your views here.


def get_profile_details(user):
    if user.user_type == UserType.VOLUNTEER:
        return Volunteer.objects.filter(user=user)

    if user.user_type == UserType.VIO:
        return Vio.objects.filter(user=user)


class LoginAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        user = authenticate(username=email, password=password)

        if user:
            if user.state == UserState.EMAIL_UNVERIFIED:
                return response.Response({"message": "User must verify email"},
                                         status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        return response.Response({"message": "Invalid credentials try again"}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerifyView(GenericAPIView):
    authentication_classes = []

    @staticmethod
    def post(request, email_token):
        print(email_token)
        if AuthService.verify_email(email_token):
            return response.Response(True, status=status.HTTP_200_OK)

        return response.Response({"message": "Invalid email token"}, status=status.HTTP_400_BAD_REQUEST)
