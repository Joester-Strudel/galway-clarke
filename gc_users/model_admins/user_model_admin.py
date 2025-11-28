# Django Imports
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

# Third-Party Imports
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin

# First-Party Imports
from ..models import GcUser


@admin.register(GcUser)
class GcUserAdmin(SimpleHistoryAdmin, ModelAdmin):
    """Admin configuration for GcUser."""

    # 1. Basic Configuration
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    ]
    list_display_links = ["email"]
    list_select_related = True
    list_per_page = 50
    list_filter = [
        "is_staff",
        "is_active",
    ]
    search_fields = [
        "email",
        "first_name",
        "last_name",
    ]
    empty_value_display = "-"
    show_facets = True

    # 2. Form Customization
    fieldsets = [
        (
            _("User Information"),
            {
                "classes": ["tab"],
                "fields": [
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "date_joined",
                ],
            },
        ),
        (
            _("Permissions"),
            {
                "classes": ["tab"],
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ],
            },
        ),
        (
            _("Metadata"),
            {
                "classes": ["tab"],
                "fields": [
                    "id",
                ],
            },
        ),
    ]

    readonly_fields = ["id", "date_joined"]

    # 4. Actions and Behavior
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True
    save_as = True
