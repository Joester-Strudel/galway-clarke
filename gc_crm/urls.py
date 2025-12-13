from django.urls import path

from .views import index_view, organizations_view, individuals_view

urlpatterns = [
    path("", index_view, name="crm-index"),
    path("organizations/", organizations_view, name="crm-organizations"),
    path("individuals/", individuals_view, name="crm-individuals"),
]
