# Django Imports
from django.urls import path
from django.views.generic import RedirectView

# First-Party Imports
from .views import index_view, organizations_view, individuals_view


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="crm-organizations", permanent=False), name="crm-index"),
    path("organizations/", organizations_view, name="crm-organizations"),
    path("individuals/", individuals_view, name="crm-individuals"),
]
