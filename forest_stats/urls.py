from django.urls import path

from forest_stats import views

urlpatterns = [
    path('stats/<district>', views.GetAllForestStats.as_view(), name="Get stats of this month and change"),
    path('images/<district>/<no_of>', views.GetImagesForDistrict.as_view(), name="Get images for district")
]
