# Django Imports
from django.contrib import admin
from django.urls import path

# First-Party Imports
from gc_core.api import api as project_api


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", project_api.urls),
]
