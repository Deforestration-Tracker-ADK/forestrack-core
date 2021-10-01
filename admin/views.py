# Create your views here.
from django.db import transaction
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from admin.forms import ApproveForm
from admin.permissions import IsAdmin
from admin.serializers import AdminRegisterSerializer
from admin.services import AdminService
from authentication.models import User
from helpers.models import get_profile_user


class AuthAdminAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    @staticmethod
    def get(request):
        # print(request)
        profile = get_profile_user(request.user)

        serializer = AdminRegisterSerializer(profile)
        return response.Response({"admin": serializer.data})


class InviteAdminView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AdminRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            if not request.data["email"]:
                return response.Response({"message": "Please add email"})

            if User.objects.filter(email=request.data["email"]).exists():
                return response.Response({"message": "NIC already exist in system"})

            admin = AdminService.createAdmin(
                request.data["email"],
                serializer.validated_data["first_name"],
                serializer.validated_data["last_name"],
                serializer.validated_data["nic"],
            )
            return response.Response(admin, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApproveOpportunity(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @staticmethod
    @transaction.atomic
    def post(request):
        form = ApproveForm(request.data, request.FILES)
        if form.is_valid():
            approve = request.data.get("approve")
            opportunity_id = request.data.get("id")
            if AdminService.approveOpportunity(opportunity_id, approve):
                return response.Response({"message": "Opportunity has been approved"},
                                         status=status.HTTP_200_OK)

            return response.Response({"message": "No such Opportunity is present OR Opportunity already approved"},
                                     status=status.HTTP_400_BAD_REQUEST)

        return response.Response({"message": form.errors}, status=status.HTTP_400_BAD_REQUEST)


class ApproveVio(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @staticmethod
    @transaction.atomic
    def post(request):
        form = ApproveForm(request.data, request.FILES)
        if form.is_valid():
            approve = request.data.get("approve")
            user_id = request.data.get("id")
            if AdminService.approveVio(user_id, approve):
                message = "Vio has been approved" if approve else "Vio has been Rejected"
                return response.Response({"message": message},
                                         status=status.HTTP_200_OK)

            return response.Response({"message": "No such Vio present or email is not verified"},
                                     status=status.HTTP_400_BAD_REQUEST)

        return response.Response({"message": form.errors}, status=status.HTTP_400_BAD_REQUEST)


class ApproveVolunteer(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @staticmethod
    @transaction.atomic
    def post(request):
        form = ApproveForm(data=request.data)
        if form.is_valid():
            approve = request.data.get("approve")
            user_id = request.data.get("id")
            if AdminService.approveVolunteer(user_id, approve):
                message = "Volunteer has been approved" if approve else "Volunteer has been Rejected"
                return response.Response({"message": message},
                                         status=status.HTTP_200_OK)

            return response.Response({"message": "No such Volunteer present or email not verified"},
                                     status=status.HTTP_400_BAD_REQUEST)

        return response.Response({"message": form.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetAdminsList(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @staticmethod
    @transaction.atomic
    def get(request):
        admins = AdminService.getListOfAdmins()
        if admins is not None:
            return response.Response(admins, status=status.HTTP_200_OK)

        return response.Response({"message": "No admins in system"}, status=status.HTTP_400_BAD_REQUEST)
