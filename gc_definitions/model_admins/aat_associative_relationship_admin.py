# Django Imports
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

# First-Party Imports
from ..models import AatAssociativeRelationship


@admin.register(AatAssociativeRelationship)
class AatAssociativeRelationshipAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_subject",
        "formatted_relationship_type",
        "formatted_related_subject",
        "formatted_historic_flag",
    ]
    list_filter = [
        "relationship_type",
        "historic_flag",
        "related_subject",
        "created_at",
    ]
    search_fields = [
        "relationship_type",
        "related_subject__aat_id",
        "historic_flag",
        "subject__aat_id",
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
                    "related_subject",
                    "historic_flag",
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

    @display(description="Subject", ordering="subject__aat_id")
    def formatted_subject(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.subject,
                    "size": "medium",
                },
            )
        )

    @display(description="Relationship Type", ordering="relationship_type")
    def formatted_relationship_type(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.relationship_type,
                    "size": "small",
                },
            )
        )

    @display(description="Related AAT ID", ordering="related_subject__aat_id")
    def formatted_related_subject(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.related_subject,
                    "size": "small",
                },
            )
        )

    @display(description="Historic Flag", ordering="historic_flag")
    def formatted_historic_flag(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.historic_flag or "N/A",
                    "size": "small",
                },
            )
        )
