from django.urls import path

from report import views

urlpatterns = [
    path('create', views.RegisterReportAPIView.as_view(), name="create report"),
    path('<district>', views.GetReportByDistrict.as_view(), name="get reports for district"),
    path('get/<report_id>', views.GetReportWithImagesById.as_view(), name="get report with details"),
]
