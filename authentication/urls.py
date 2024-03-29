from django.urls import path

from . import views

urlpatterns = [
    path('login', views.LoginAPIView.as_view(), name="Login"),
    path('email_verify/<email_token>', views.EmailVerifyView.as_view(), name="email_verify"),
    path('change/password', views.ChangePasswordView.as_view(), name="email_verify")
]
