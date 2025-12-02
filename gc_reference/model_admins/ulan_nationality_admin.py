# Django Imports
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

# First-Party Imports
from ..models import UlanNationality


@admin.register(UlanNationality)
class UlanNationalityAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_subject",
        "formatted_nationality_code",
        "formatted_display_order",
        "formatted_is_preferred",
    ]
    list_filter = [
        "is_preferred",
        "created_at",
    ]
    search_fields = [
        "nationality_code",
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
                    "nationality_code",
                    "display_order",
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

    @display(description="Nationality", ordering="nationality_code")
    def formatted_nationality_code(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.nationality_code, "size": "small"},
            )
        )

    @display(description="Display Order", ordering="display_order")
    def formatted_display_order(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.display_order
                    if obj.display_order is not None
                    else "N/A",
                    "size": "small",
                },
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
