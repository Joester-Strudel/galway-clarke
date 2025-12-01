# Django Imports
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

# First-Party Imports
from ..models import UlanAssociativeRelationship


@admin.register(UlanAssociativeRelationship)
class UlanAssociativeRelationshipAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_subject",
        "formatted_relationship_type",
        "formatted_related_ulan_id",
        "formatted_display_date",
    ]
    list_filter = [
        "relationship_type",
        "historic_flag",
        "created_at",
    ]
    search_fields = [
        "relationship_type",
        "related_ulan_id",
        "historic_flag",
        "display_date",
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
                    "relationship_type",
                    "related_ulan_id",
                    "historic_flag",
                    "display_date",
                    "start_date",
                    "end_date",
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

    @display(description="Relationship Type", ordering="relationship_type")
    def formatted_relationship_type(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.relationship_type, "size": "small"},
            )
        )

    @display(description="Related ULAN ID", ordering="related_ulan_id")
    def formatted_related_ulan_id(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.related_ulan_id, "size": "small"},
            )
        )

    @display(description="Display Date", ordering="display_date")
    def formatted_display_date(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.display_date or "N/A", "size": "small"},
            )
        )
