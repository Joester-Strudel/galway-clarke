# Django Imports
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

# First-Party Imports
from ..models import UlanRole


@admin.register(UlanRole)
class UlanRoleAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_subject",
        "formatted_role_id",
        "formatted_is_preferred",
        "formatted_historic_flag",
    ]
    list_filter = [
        "is_preferred",
        "historic_flag",
        "created_at",
    ]
    search_fields = [
        "role_id",
        "historic_flag",
        "subject__ulan_id",
    ]
    ordering = [
        "-created_at",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "last_updated_at",
        "created_by",
    ]

    # Fieldsets for better organization
    fieldsets = (
        (
            _("General Information"),
            {
                "classes": ["tab"],
                "fields": [
                    "subject",
                    "role_id",
                    "historic_flag",
                    "is_preferred",
                ],
            },
        ),
        (
            _("Metadata"),
            {
                "classes": ["tab"],
                "fields": [
                    "id",
                    "created_at",
                    "last_updated_at",
                    "created_by",
                ],
            },
        ),
    )

    @display(description="Subject", ordering="subject__ulan_id")
    def formatted_subject(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.subject, "size": "medium"},
            )
        )

    @display(description="Role ID", ordering="role_id")
    def formatted_role_id(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.role_id, "size": "small"},
            )
        )

    @display(description="Preferred", ordering="is_preferred")
    def formatted_is_preferred(self, obj):
        options = {
            True: {"label": "Preferred", "icon": "check_circle", "color": "green"},
            False: {"label": "Not preferred", "icon": "cancel", "color": "slate"},
        }
        option = options[obj.is_preferred]
        return mark_safe(
            render_to_string(
                "admin/badge.html",
                {
                    "label": option["label"],
                    "icon": option["icon"],
                    "color": option["color"],
                },
            )
        )

    @display(description="Historic Flag", ordering="historic_flag")
    def formatted_historic_flag(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.historic_flag or "N/A", "size": "small"},
            )
        )
