# Create your views here.
from django.core.exceptions import BadRequest
from django.db import transaction
from rest_framework import response, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from admin.forms import ApproveForm
from admin.helpers import create_admin
from admin.services import AdminService


class InviteAdminView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def post(request):
        try:
            if "email" not in request.data:
                raise BadRequest("No email Provided")

            admin_email = request.data["email"]
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
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    @transaction.atomic
    def post(request, opportunity_id):
        form = ApproveForm(request.POST, request.FILES)
        if form.is_valid():
            approve = request.POST.get("approve")
            opportunity_id = opportunity_id
            if AdminService.approveOpportunity(opportunity_id, approve):
                return response.Response({"message": "Opportunity has been approved"},
                                         status=status.HTTP_200_OK)

            return response.Response({"message": "No such Opportunity is present"},
                                     status=status.HTTP_400_BAD_REQUEST)

        return response.Response({"message": form.errors}, status=status.HTTP_400_BAD_REQUEST)


class ApproveVio(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    @transaction.atomic
    def post(request, user_id):
        form = ApproveForm(request.POST, request.FILES)
        if form.is_valid():
            approve = request.POST.get("approve")
            if AdminService.approveVio(user_id, approve):
                return response.Response({"message": "Vio has been approved"},
                                         status=status.HTTP_200_OK)

            return response.Response({"message": "No such Volunteer present"},
                                     status=status.HTTP_400_BAD_REQUEST)

        return response.Response({"message": form.errors}, status=status.HTTP_400_BAD_REQUEST)


class ApproveVolunteer(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    @transaction.atomic
    def post(request, user_id):
        form = ApproveForm(request.POST, request.FILES)
        if form.is_valid():
            approve = request.POST.get("approve")
            if AdminService.approveVolunteer(user_id, approve):
                return response.Response({"message": "Vio has been approved"},
                                         status=status.HTTP_200_OK)

            return response.Response({"message": "No such Volunteer present"},
                                     status=status.HTTP_400_BAD_REQUEST)

        return response.Response({"message": form.errors}, status=status.HTTP_400_BAD_REQUEST)
