from django.urls import path

from report import views

urlpatterns = [
    path('create', views.RegisterReportAPIView.as_view(), name="vio_register"),
    path('<district>', views.GetReportByDistrict.as_view(), name="vio_register"),
    path('get/<report_id>', views.GetReportWithImagesById.as_view(), name="vio_register"),
]
