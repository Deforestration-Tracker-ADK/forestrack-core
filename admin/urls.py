from django.urls import path

from admin import views

urlpatterns = [
    path("create", views.InviteAdminView.as_view(), name="create_new_admin"),
    path("approve/volunteer", views.ApproveVolunteer.as_view(), name="admin_approve_volunteer"),
    path("approve/vio", views.ApproveVio.as_view(), name="admin_approve_vio"),
    path("approve/opportunity", views.ApproveOpportunity.as_view(), name="admin_approve_opportunity"),
    path("allAdmins", views.GetAdminsList.as_view(), name="Get_all_admins")
]
