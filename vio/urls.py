from django.urls import path

from vio import views

urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name="vio_register"),
    path('get/<vio_id>', views.GetVioByID.as_view(), name="get vio by id"),
    path('view', views.AuthVioAPIView.as_view(), name="get_data_using_token"),
    path('approve/volunteer', views.AcceptVolunteerForOpportunity.as_view(), name="approve_volunteer_opportunity"),
    path('approved', views.GetAllApprovedVio.as_view(), name="Get approved Vio"),
    path("unapproved", views.GetAllUnapprovedVio.as_view(), name="Get unapproved vio"),
]
