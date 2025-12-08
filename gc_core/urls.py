# Django Imports
from django.contrib import admin
from django.urls import path

# First-Party Imports
from gc_users.views.signin_view import signin
from gc_users.views.signout_view import signout
from gc_users.views.signup_view import signup
from gc_users.views.select_organization_view import select_organization
from gc_users.views.create_organization_view import create_organization
from gc_users.views.update_preferences_view import update_preferences
from gc_core.views.index_view import index
from gc_dashboard.views.get_dashboard_index import get_dashboard_index
from gc_crm.views.get_crm_index import get_crm_index


urlpatterns = [
    path("", index, name="marketing-home"),
    path("dashboard/", get_dashboard_index, name="dashboard-index"),
    path("crm/", get_crm_index, name="crm-index"),
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    path("select-organization/", select_organization, name="select-organization"),
    path("create-organization/", create_organization, name="create-organization"),
    path("user/preferences/", update_preferences, name="user-preferences"),
    path("admin/", admin.site.urls),
]
