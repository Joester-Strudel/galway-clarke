# Django Imports
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

# First-Party Imports
from ..models import UlanSubject


@admin.register(UlanSubject)
class UlanSubjectAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_ulan_id",
        "formatted_record_type",
        "formatted_parent",
        "formatted_parent_relationship_type",
        "formatted_merged_status",
    ]
    list_filter = [
        "record_type",
        "merged_status",
        "parent_relationship_type",
        "parent",
        "created_at",
    ]
    search_fields = [
        "ulan_id",
        "record_type__name",
        "parent__ulan_id",
        "parent_string",
        "parent_relationship_type__name",
    ]
    ordering = [
        "ulan_id",
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
                    "ulan_id",
                    "record_type",
                    "merged_status",
                    "parent",
                    "parent_relationship_type",
                    "parent_string",
                    "parent_historic_flag",
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

    @display(description="ULAN ID", ordering="ulan_id")
    def formatted_ulan_id(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.ulan_id, "size": "medium"},
            )
        )

    @display(description="Record Type", ordering="record_type")
    def formatted_record_type(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.record_type or "N/A", "size": "small"},
            )
        )

    @display(description="Parent ULAN ID", ordering="parent__ulan_id")
    def formatted_parent(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.parent or "N/A", "size": "small"},
            )
        )

    @display(description="Parent Relationship", ordering="parent_relationship_type")
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
                {"value": obj.merged_status or "N/A", "size": "small"},
            )
        )
