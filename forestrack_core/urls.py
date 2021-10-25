"""forestrack_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# create_core_admin()

schema_view = get_schema_view(
    openapi.Info(
        title="Forestrack API",
        default_version="v1",
        description="API for the forestrack system.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="devin.18@cse.mrt.ac.lk", name="Devin De Silva"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/opportunity/', include('opportunity.urls')),
    path('api/forest_stats/', include('forest_stats.urls')),
    path('api/reports/', include('report.urls')),
    path('api/auth/', include('authentication.urls')),
    path('api/volunteer/', include('volunteer.urls')),
    path('api/admin/', include('admin.urls')),
    path('api/vio/', include('vio.urls')),
]
