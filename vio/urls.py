from django.urls import path

from vio import views

urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name="vio_register"),
    path('view', views.AuthVioAPIView.as_view(), name="get_data_using_token"),
    path('approve/volunteer', views.AcceptVolunteerForOpportunity.as_view(), name="approve_volunteer_opportunity")
]
