from django.urls import path

from opportunity import views

urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name="opportunity_register"),
    path("approved", views.GetApprovedOpportunity.as_view(), name="get_opportunities_approved"),
    path("unapproved", views.GetUnapprovedOpportunity.as_view(), name="get_opportunities_unapproved"),
]
