# Create your views here.
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView

from helpers.models import get_profile_user
from opportunity.serializers import ApplyForOpportunitySerializer
from volunteer.serializers import VolunteerRegisterSerializer


class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = VolunteerRegisterSerializer

    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthVolunteerAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request):
        # print(request)
        profile = get_profile_user(request.user)

        serializer = VolunteerRegisterSerializer(profile)
        return response.Response({"volunteer": serializer.data})


class ApplyForOpportunityAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ApplyForOpportunitySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
