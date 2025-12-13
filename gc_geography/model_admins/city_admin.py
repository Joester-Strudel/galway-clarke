# Django Imports
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from unfold.admin import ModelAdmin, display

# First-Party Imports
from ..models import City


@admin.register(City)
class CityAdmin(ModelAdmin):
    """Admin configuration for cities."""

    list_display = [
        "name",
        "formatted_state",
        "formatted_county",
        "created_at",
        "last_updated_at",
    ]
    list_filter = [
        "state",
        "county",
        "created_at",
        "last_updated_at",
    ]
    search_fields = [
        "name",
    ]
    ordering = ["state", "name"]
    readonly_fields = [
        "id",
        "created_at",
        "last_updated_at",
        "created_by",
    ]

    fieldsets = [
        (
            _("City"),
            {
                "classes": ["tab"],
                "fields": [
                    "name",
                    "state",
                    "county",
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

    @display(description=_("State"), ordering="state__name")
    def formatted_state(self, obj):
        return getattr(obj.state, "name", "-")

    @display(description=_("County"), ordering="county__name")
    def formatted_county(self, obj):
        return getattr(obj.county, "name", "-")
