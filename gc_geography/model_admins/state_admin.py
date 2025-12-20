# Django Imports
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from unfold.admin import ModelAdmin, display

# First-Party Imports
from ..models import State


@admin.register(State)
class StateAdmin(ModelAdmin):
    """Admin configuration for states."""

    list_display = [
        "formatted_name",
        "formatted_abbreviation",
        "created_at",
        "last_updated_at",
    ]
    list_filter = [
        "created_at",
        "last_updated_at",
    ]
    search_fields = [
        "name",
        "abbreviation",
    ]
    ordering = ["name"]
    readonly_fields = [
        "id",
        "created_at",
        "last_updated_at",
        "created_by",
    ]

    fieldsets = [
        (
            _("State"),
            {
                "classes": ["tab"],
                "fields": [
                    "name",
                    "abbreviation",
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
    ]

    @display(description=_("Name"), ordering="name")
    def formatted_name(self, obj):
        return mark_safe(
            render_to_string(
                "cotton/admin/components/text.html",
                {
                    "value": obj.name,
                    "size": "medium",
                },
            )
        )

    @display(description=_("Abbreviation"), ordering="abbreviation")
    def formatted_abbreviation(self, obj):
        return mark_safe(
            render_to_string(
                "cotton/admin/components/text.html",
                {
                    "value": obj.abbreviation or "—",
                    "size": "small",
                },
            )
        )
