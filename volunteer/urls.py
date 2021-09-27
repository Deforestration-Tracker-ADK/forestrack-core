from django.urls import path

from volunteer import views

urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name="volunteer_register"),
    path('view', views.AuthVolunteerAPIView.as_view(), name="get_data_using_token"),
    path('opportunity/apply', views.ApplyForOpportunityAPIView.as_view(), name="apply_opportunity"),
    path('approved', views.GetAllApprovedVolunteer.as_view(), name="Get approved Volunteer"),
    path("unapproved", views.GetAllUnapprovedVolunteer.as_view(), name="Get unapproved volunteer"),
]
