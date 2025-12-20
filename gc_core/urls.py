# Django Imports
from django.contrib import admin
from django.urls import path, include

# First-Party Imports
from gc_core.views.index_view import index
from gc_dashboard.views.get_dashboard_index import get_dashboard_index


urlpatterns = [
    path("", index, name="marketing-home"),
    path("dashboard/", get_dashboard_index, name="dashboard-index"),
    path("crm/", include("gc_crm.urls")),
    path("", include("gc_users.urls")),
    path("select2/", include("django_select2.urls")),
    path("admin/", admin.site.urls),
]
