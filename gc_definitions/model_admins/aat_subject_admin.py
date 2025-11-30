# Django Imports
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

# First-Party Imports
from ..inlines import (
    AATAssociativeRelationshipInline,
    AATNoteInline,
    AATSubjectContributorInline,
    AATSubjectSourceInline,
    AATTermInline,
)
from ..models import AATSubject


@admin.register(AATSubject)
class AATSubjectAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_aat_id",
        "formatted_record_type",
        "formatted_parent_aat_id",
        "formatted_parent_relationship_type",
        "formatted_merged_status",
    ]
    list_filter = [
        "record_type",
        "merged_status",
        "parent_relationship_type",
        "created_at",
    ]
    search_fields = [
        "aat_id",
        "parent_aat_id",
        "parent_string",
        "parent_relationship_type",
    ]
    ordering = [
        "aat_id",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "last_updated_at",
        "created_by",
    ]

    inlines = [
        AATTermInline,
        AATNoteInline,
        AATSubjectContributorInline,
        AATSubjectSourceInline,
        AATAssociativeRelationshipInline,
    ]

    # Fieldsets for better organization
    fieldsets = (
        (
            _("General Information"),
            {
                "classes": ["tab"],
                "fields": [
                    "aat_id",
                    "record_type",
                    "merged_status",
                    "sort_order",
                    "parent_aat_id",
                    "parent_relationship_type",
                    "parent_string",
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

    @display(description="AAT ID", ordering="aat_id")
    def formatted_aat_id(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.aat_id,
                    "size": "medium",
                },
            )
        )

    @display(description="Record Type", ordering="record_type")
    def formatted_record_type(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.record_type or "N/A",
                    "size": "small",
                },
            )
        )

    @display(description="Parent AAT ID", ordering="parent_aat_id")
    def formatted_parent_aat_id(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.parent_aat_id or "N/A",
                    "size": "small",
                },
            )
        )

    @display(
        description="Parent Relationship Type", ordering="parent_relationship_type"
    )
    def formatted_parent_relationship_type(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.parent_relationship_type or "N/A",
                    "size": "small",
                },
            )
        )

    @display(description="Merged Status", ordering="merged_status")
    def formatted_merged_status(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.merged_status or "N/A",
                    "size": "small",
                },
            )
        )
