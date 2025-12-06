# Django Imports
from django.contrib import admin
from django.urls import path

# First-Party Imports
from gc_core.api import api as project_api
from gc_core.views.index_view import index


urlpatterns = [
    path("", index, name="marketing-home"),
    path("admin/", admin.site.urls),
    path("api/", project_api.urls),
]
