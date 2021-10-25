# Create your views here.
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView

from authentication.enums import VolunteerVioState
from helpers.models import get_profile_user
from opportunity.serializers import ApplyForOpportunitySerializer
from volunteer.permissions import IsVolunteer
from volunteer.serializers import VolunteerRegisterSerializer
from volunteer.services import VolunteerService


class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = VolunteerRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthVolunteerAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsVolunteer)

    @staticmethod
    def get(request):
        # print(request)
        profile = get_profile_user(request.user)

        serializer = VolunteerRegisterSerializer(profile)
        return response.Response({"volunteer": serializer.data})


class ApplyForOpportunityAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsVolunteer]
    serializer_class = ApplyForOpportunitySerializer

    def post(self, request):
        request.data["volunteer_id"] = request.user.id
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllApprovedVolunteer(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request):
        return response.Response(VolunteerService.getVolunteer(state=VolunteerVioState.APPROVED),
                                 status=status.HTTP_200_OK)


class GetAllUnapprovedVolunteer(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request):
        return response.Response(VolunteerService.getVolunteer(state=VolunteerVioState.UNAPPROVED),
                                 status=status.HTTP_200_OK)


class GetVolunteerByID(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request, volunteer_id):
        return response.Response(VolunteerService.getVolunteerById(volunteer_id),
                                 status=status.HTTP_200_OK)
