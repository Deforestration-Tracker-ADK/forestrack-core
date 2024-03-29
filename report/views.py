# Create your views here.
import os

import cloudinary
from dotenv import load_dotenv
from rest_framework import permissions, response, status
from rest_framework.generics import GenericAPIView

from forest_stats.enum import district_location_Map
from report.forms import ReportForm
from report.models import DeforestationReport, ReportPhoto
from report.services import ReportService
from volunteer.models import Volunteer
from volunteer.permissions import IsVolunteer

load_dotenv()

cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)


class RegisterReportAPIView(GenericAPIView):
    """
    Create a Report.
    """
    permission_classes = (permissions.IsAuthenticated, IsVolunteer)

    @staticmethod
    def post(request):
        post_form = ReportForm(data=request.data)
        images = request.FILES.getlist("images", None)

        if not post_form.is_valid():
            return response.Response(post_form.errors, status=status.HTTP_400_BAD_REQUEST)

        data = {}
        long = request.data.get("long", None)
        district = request.data.get("district", None)

        if district is None:
            return response.Response({"district": "Please select a district"}, status=status.HTTP_400_BAD_REQUEST)

        # if the long and lat is not available in data map long lat from defined enum in enum.py file
        if long is None:
            data["long"] = district_location_Map[district][0]
            data["lat"] = district_location_Map[district][1]

        data["volunteer"] = Volunteer.objects.get(user_id=request.user.id)
        data["title"] = request.data.get("title")
        data["severity"] = request.data.get("severity")
        data["district"] = request.data.get("district")
        data["recent"] = request.data.get("recent")
        data["action_description"] = request.data.get("action_description")
        data["special_notes"] = request.data.get("special_notes")
        data["location"] = request.data.get("location")
        report = DeforestationReport.objects.create(**data)

        # store each image in the Cloudinary API
        if images:
            for image in images:
                ReportPhoto.objects.create(
                    report=report,
                    image=image,
                )

        return response.Response({"message": "report successfully created"}, status=status.HTTP_201_CREATED)


class GetReportByDistrict(GenericAPIView):
    """
    Get the reports of a specific district.
    """
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def get(request, district):
        if district is None:
            return response.Response({"district": "Please select a district"}, status=status.HTTP_400_BAD_REQUEST)

        reports = ReportService.get_reports_without_images(district)

        return response.Response(reports, status=status.HTTP_200_OK)


class GetReportWithImagesById(GenericAPIView):
    """
    Get Report with images of a particular report.
    """
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def get(request, report_id):
        report = ReportService.get_reports_with_image(report_id)

        if report is None:
            return response.Response({"report_id": "No such report"}, status=status.HTTP_400_BAD_REQUEST)

        return response.Response(report, status=status.HTTP_200_OK)
