# Django Imports
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from unfold.admin import ModelAdmin, display

# First-Party Imports
from ..models import Industry


@admin.register(Industry)
class IndustryAdmin(ModelAdmin):
    """Admin configuration for CRM industries."""

    list_display = [
        "name",
        "formatted_team",
        "created_at",
        "last_updated_at",
    ]
    list_filter = [
        "team",
        "created_at",
        "last_updated_at",
    ]
    search_fields = [
        "name",
        "description",
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
            _("Industry"),
            {
                "classes": ["tab"],
                "fields": [
                    "name",
                    "team",
                    "description",
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

    @display(description=_("Team"), ordering="team__name")
    def formatted_team(self, obj):
        return getattr(obj.team, "name", "-")
