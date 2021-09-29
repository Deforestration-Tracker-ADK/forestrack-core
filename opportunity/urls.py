from django.urls import path

from opportunity import views

urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name="opportunity_register"),
    path("approved", views.GetApprovedOpportunity.as_view(), name="get_opportunities_approved"),
    path("<opportunity_id>", views.GetOpportunityById.as_view(), name="get_opportunity_by_id"),
    path("unapproved", views.GetUnapprovedOpportunity.as_view(), name="get_opportunities_unapproved"),
    path("volunteer/accepted/<vol_id>", views.GetVolunteerAcceptedProjectsForVolunteer.as_view(),
         name="get_volunteer_approved_projects"),
    path("volunteer/pending/<vol_id>", views.GetVolunteerPendingProjectsForVolunteer.as_view(),
         name="get_volunteer_pending_projects"),
    path("volunteer/completed/<vol_id>", views.GetVolunteerCompletedProjectsForVolunteer.as_view(),
         name="get_volunteer_completed_projects"),
    path("accepted/volunteers/<opportunity_id>", views.GetAcceptedVolunteersForOpportunity.as_view(),
         name="get_volunteers_pending_for_projects"),
    path("11pending/volunteers/<opportunity_id>", views.GetPendingVolunteersForOpportunity.as_view(),
         name="get_volunteers_accepted_for_projects"),
]
