# Django Imports
from django.urls import path

# First-Party Imports
from .views import (
    index_view,
    organizations_view,
    individuals_view,
    organization_drawer_view,
    organization_create_view,
    organization_delete_view,
    individual_drawer_view,
    individual_create_view,
    individual_delete_view,
    select_statuses,
    select_tags,
    select_industries,
    select_organizations,
    select_cities,
    select_states,
    select_counties,
    select_zip_codes,
    select_individuals,
)


urlpatterns = [
    path("", index_view, name="crm-index"),
    path("organizations/", organizations_view, name="crm-organizations"),
    path("individuals/", individuals_view, name="crm-individuals"),
    path(
        "organizations/<uuid:org_id>/edit/",
        organization_drawer_view,
        name="crm-organization-edit",
    ),
    path(
        "organizations/new/",
        organization_create_view,
        name="crm-organization-create",
    ),
    path(
        "organizations/<uuid:org_id>/delete/",
        organization_delete_view,
        name="crm-organization-delete",
    ),
    path(
        "individuals/<uuid:individual_id>/edit/",
        individual_drawer_view,
        name="crm-individual-edit",
    ),
    path(
        "individuals/new/",
        individual_create_view,
        name="crm-individual-create",
    ),
    path(
        "individuals/<uuid:individual_id>/delete/",
        individual_delete_view,
        name="crm-individual-delete",
    ),
    path("select/statuses/", select_statuses, name="crm-select-statuses"),
    path("select/tags/", select_tags, name="crm-select-tags"),
    path("select/industries/", select_industries, name="crm-select-industries"),
    path("select/organizations/", select_organizations, name="crm-select-organizations"),
    path("select/cities/", select_cities, name="crm-select-cities"),
    path("select/states/", select_states, name="crm-select-states"),
    path("select/counties/", select_counties, name="crm-select-counties"),
    path("select/zip-codes/", select_zip_codes, name="crm-select-zip-codes"),
    path("select/individuals/", select_individuals, name="crm-select-individuals"),
]
