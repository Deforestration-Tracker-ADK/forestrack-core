from django.urls import path

from admin import views

urlpatterns = [
    path("create", views.InviteAdminView.as_view(), name="create_new_admin"),
    path("approve/volunteer/<user_id>", views.ApproveVolunteer.as_view(), name="admin_approve_volunteer"),
    path("approve/vio/<user_id>", views.ApproveVio.as_view(), name="admin_approve_vio"),
    path("approve/opportunity/<opportunity_id>", views.ApproveOpportunity.as_view(), name="admin_approve_opportunity")
]
