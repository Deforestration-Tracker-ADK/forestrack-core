# Create your views here.
from django.core.exceptions import BadRequest
from django.db import transaction
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from admin.forms import ApproveForm
from admin.helpers import create_admin
from admin.permissions import IsAdmin
from admin.services import AdminService
from authentication.models import User


class InviteAdminView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @staticmethod
    def post(request):
        try:
            if "email" not in request.data:
                raise BadRequest("No email Provided")

            admin_email = request.data["email"]
            if User.objects.filter(email=admin_email):
                return response.Response({"message": "User with same email already exist in system"},
                                         status=status.HTTP_400_BAD_REQUEST)
            admin = create_admin(admin_email)
            if admin:
                return response.Response({"message": "Successfully invited admin"}, status=status.HTTP_200_OK)

            return response.Response({"message": "Error when creating admin"}, status=status.HTTP_400_BAD_REQUEST)

        except BadRequest as error:
            return response.Response({"message": "No email provided"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print(error)
            return response.Response({"message": "Error when creating admin"}, status=status.HTTP_400_BAD_REQUEST)


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
