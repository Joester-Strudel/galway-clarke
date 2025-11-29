# Django Imports
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, display

# First-Party Imports
from ..models import Organization


@admin.register(Organization)
class OrganizationAdmin(SimpleHistoryAdmin, ModelAdmin):
    """Admin configuration for Organization."""

    list_display = [
        "formatted_name",
        "created_at",
        "last_updated_at",
    ]
    list_filter = [
        "created_at",
    ]
    search_fields = [
        "name",
    ]
    ordering = [
        "name",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "last_updated_at",
        "created_by",
    ]

    fieldsets = (
        (
            _("General Information"),
            {
                "classes": ["tab"],
                "fields": [
                    "name",
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

    @display(description="Name", ordering="name")
    def formatted_name(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.name,
                    "size": "large",
                },
            )
        )
