from django.urls import path

from .views import get_crm_index, get_crm_organizations, get_crm_individuals

urlpatterns = [
    path("", get_crm_index, name="crm-index"),
    path("organizations/", get_crm_organizations, name="crm-organizations"),
    path("individuals/", get_crm_individuals, name="crm-individuals"),
]
