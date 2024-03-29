from django.urls import path

from opportunity import views

urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name="opportunity_register"),
    path("approved", views.GetApprovedOpportunity.as_view(), name="get_opportunities_approved"),
    path("getOpportunity/<opportunity_id>", views.GetOpportunityById.as_view(), name="get_opportunity_by_id"),
    path("completeOpportunity/<opportunity_id>", views.CompleteOpportunityById.as_view(),
         name="complete_opportunity_by_id"),
    path("get/unapproved", views.GetUnapprovedOpportunity.as_view(), name="get_opportunities_unapproved"),
    path("vio/<vio_id>", views.GetOpportunityByForVio.as_view(), name="Get Opportunity for Vio"),
    path("vio/unaccepted/<vio_id>", views.GetUnapprovedOpportunityForVio.as_view(), name="Get Opportunity for Vio"),
    path("vio/approved/<vio_id>", views.GetApprovedOpportunityForVio.as_view(),
         name="Get Approved opportunities for Vio"),
    path("vio/completed/<vio_id>", views.GetCompletedOpportunityForVio.as_view(),
         name="Get Approved opportunities for Vio"),
    path("getVolOpp/<vol_opp_id>", views.GetVolOppFromId.as_view(), name="get a volunteer opportunity from Id"),
    path("volunteer/accepted/<vol_id>", views.GetVolunteerAcceptedProjectsForVolunteer.as_view(),
         name="get_volunteer_approved_projects"),
    path("volunteer/pending/<vol_id>", views.GetVolunteerPendingProjectsForVolunteer.as_view(),
         name="get_volunteer_pending_projects"),
    path("volunteer/completed/<vol_id>", views.GetVolunteerCompletedProjectsForVolunteer.as_view(),
         name="get_volunteer_completed_projects"),
    path("accepted/volunteers/<opportunity_id>", views.GetAcceptedVolunteersForOpportunity.as_view(),
         name="get_volunteers_pending_for_projects"),
    path("pending/volunteers/<opportunity_id>", views.GetPendingVolunteersForOpportunity.as_view(),
         name="get_volunteers_accepted_for_projects"),
    path("completed/volunteers/<opportunity_id>", views.GetCompletedVolunteersForOpportunity.as_view(),
         name="get_volunteers_completed_for_projects"),
    path("search", views.SearchOpportunity.as_view(), name="Search title"),
    path("search/volunteer", views.SearchOpportunityVolunteer.as_view(), name="Search Opportunities for a Volunteer")
]
