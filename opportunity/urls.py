from django.urls import path

from opportunity import views

urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name="opportunity_register"),
]
