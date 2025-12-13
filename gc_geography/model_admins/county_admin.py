# Django Imports
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from unfold.admin import ModelAdmin, display

# First-Party Imports
from ..models import County


@admin.register(County)
class CountyAdmin(ModelAdmin):
    """Admin configuration for counties."""

    list_display = [
        "name",
        "fips_code",
        "formatted_state",
        "created_at",
        "last_updated_at",
    ]
    list_filter = [
        "state",
        "created_at",
        "last_updated_at",
    ]
    search_fields = [
        "name",
        "fips_code",
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
            _("County"),
            {
                "classes": ["tab"],
                "fields": [
                    "name",
                    "fips_code",
                    "state",
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
