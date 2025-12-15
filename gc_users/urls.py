from django.urls import path

from gc_users.views.signin_view import signin
from gc_users.views.signout_view import signout
from gc_users.views.signup_view import signup
from gc_users.views.select_organization_view import select_organization
from gc_users.views.create_team_view import create_team
from gc_users.views.update_preferences_view import update_preferences
from gc_users.views.team_settings_view import team_settings
from gc_users.views.team_statuses_view import (
    team_status_drawer,
    create_status,
    update_status,
    delete_status,
)
from gc_users.views.team_tags_view import (
    team_tags_drawer,
    create_tag,
    update_tag,
    delete_tag,
)
from gc_users.views.team_industries_view import (
    team_industries_drawer,
    create_industry,
    update_industry,
    delete_industry,
)

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    path("select-organization/", select_organization, name="select-organization"),
    path("create-team/", create_team, name="create-team"),
    path("user/preferences/", update_preferences, name="user-preferences"),
    path("settings/", team_settings, name="settings"),
    path("settings/members/", team_settings, {"tab": "members"}, name="settings-members"),
    path(
        "settings/field-definitions/",
        team_settings,
        {"tab": "field-definitions"},
        name="settings-field-definitions",
    ),
    path("settings/statuses/", team_status_drawer, name="settings-statuses"),
    path("settings/statuses/create/", create_status, name="settings-status-create"),
    path(
        "settings/statuses/<uuid:status_id>/update/",
        update_status,
        name="settings-status-update",
    ),
    path(
        "settings/statuses/<uuid:status_id>/delete/",
        delete_status,
        name="settings-status-delete",
    ),
    path("settings/tags/", team_tags_drawer, name="settings-tags"),
    path("settings/tags/create/", create_tag, name="settings-tag-create"),
    path(
        "settings/tags/<uuid:tag_id>/update/",
        update_tag,
        name="settings-tag-update",
    ),
    path(
        "settings/tags/<uuid:tag_id>/delete/",
        delete_tag,
        name="settings-tag-delete",
    ),
    path("settings/industries/", team_industries_drawer, name="settings-industries"),
    path("settings/industries/create/", create_industry, name="settings-industry-create"),
    path(
        "settings/industries/<uuid:industry_id>/update/",
        update_industry,
        name="settings-industry-update",
    ),
    path(
        "settings/industries/<uuid:industry_id>/delete/",
        delete_industry,
        name="settings-industry-delete",
    ),
]
