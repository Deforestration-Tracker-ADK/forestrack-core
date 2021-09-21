# Create your views here.
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView

from helpers.models import get_profile_user
from vio.forms import AcceptVolunteerOpportunity
from vio.serializers import VioRegisterSerializer
from vio.services import VioService


class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = VioRegisterSerializer

    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthVioAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request):
        # print(request)
        profile = get_profile_user(request.user)

        serializer = VioRegisterSerializer(profile)
        return response.Response({"vio": serializer.data})


class AcceptVolunteerForOpportunity(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        form = AcceptVolunteerOpportunity(request.POST, request.FILES)
        if form.is_valid():
            approve = request.POST.get("approve")
            volunteer_id = request.POST.get("volunteer_id")
            opportunity_id = request.POST.get("opportunity_id")
            if VioService.approveVolunteerForOpportunity(volunteer_id, opportunity_id, approve, request.user):
                return response.Response({"message": "Volunteer has been approved"},
                                         status=status.HTTP_200_OK)

            return response.Response({"message": "No such Volunteer Request for this volunteer present"},
                                     status=status.HTTP_400_BAD_REQUEST)

        return response.Response({"message": form.errors}, status=status.HTTP_400_BAD_REQUEST)
