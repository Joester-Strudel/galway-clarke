# Django Imports
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from unfold.admin import ModelAdmin, display

# First-Party Imports
from ..models import State


@admin.register(State)
class StateAdmin(ModelAdmin):
    """Admin configuration for states."""

    list_display = [
        "name",
        "abbreviation",
        "economic_nexus",
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
                    "economic_nexus",
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
