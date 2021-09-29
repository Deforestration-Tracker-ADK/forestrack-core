# Create your views here.
from django.db import transaction
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from admin.forms import ApproveForm
from admin.permissions import IsAdmin
from admin.serializers import AdminRegisterSerializer
from admin.services import AdminService


class InviteAdminView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AdminRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

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
                return response.Response({"message": "Vio has been approved"},
                                         status=status.HTTP_200_OK)

            return response.Response({"message": "No such Vio present or email is not verified"},
                                     status=status.HTTP_400_BAD_REQUEST)

        return response.Response({"message": form.errors}, status=status.HTTP_400_BAD_REQUEST)


class ApproveVolunteer(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @staticmethod
    @transaction.atomic
    def post(request):
        form = ApproveForm(request.data, request.FILES)
        if form.is_valid():
            approve = request.data.get("approve")
            user_id = request.data.get("id")
            if AdminService.approveVolunteer(user_id, approve):
                return response.Response({"message": "Volunteer has been approved"},
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