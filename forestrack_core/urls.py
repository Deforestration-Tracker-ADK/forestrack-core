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
from django.conf.urls import url
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from admin.helpers import create_core_admin

create_core_admin()
schema_view = get_swagger_view(title='ForestRack API')

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', schema_view),
    path('api/opportunity/', include('opportunity.urls')),
    path('api/forest_stats/', include('forest_stats.urls')),
    path('api/reports/', include('report.urls')),
    path('api/auth/', include('authentication.urls')),
    path('api/volunteer/', include('volunteer.urls')),
    path('api/admin/', include('admin.urls')),
    path('api/vio/', include('vio.urls')),
]
