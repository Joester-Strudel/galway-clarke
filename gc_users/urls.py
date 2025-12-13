from django.urls import path

from gc_users.views.signin_view import signin
from gc_users.views.signout_view import signout
from gc_users.views.signup_view import signup
from gc_users.views.select_organization_view import select_organization
from gc_users.views.create_team_view import create_team
from gc_users.views.update_preferences_view import update_preferences

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    path("select-organization/", select_organization, name="select-organization"),
    path("create-team/", create_team, name="create-team"),
    path("user/preferences/", update_preferences, name="user-preferences"),
]
