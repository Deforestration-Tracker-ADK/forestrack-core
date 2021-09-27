from django.urls import path

from forest_stats import views

urlpatterns = [
    path('lastmonth', views.GetAllForestStats.as_view(), name=""),
]
