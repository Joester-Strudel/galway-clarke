# Django Imports
from django.contrib import admin
from django.urls import path

# First-Party Imports
from gc_users.views.signin_view import signin
from gc_users.views.signout_view import signout
from gc_users.views.signup_view import signup
from gc_users.views.select_organization_view import select_organization
from gc_users.views.create_organization_view import create_organization
from gc_core.views.index_view import index


urlpatterns = [
    path("", index, name="marketing-home"),
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    path("select-organization/", select_organization, name="select-organization"),
    path("create-organization/", create_organization, name="create-organization"),
    path("admin/", admin.site.urls),
]
