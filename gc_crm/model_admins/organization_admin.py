# Django Imports
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from unfold.admin import ModelAdmin, display

# First-Party Imports
from ..models import Organization


@admin.register(Organization)
class OrganizationAdmin(ModelAdmin):
    """Admin configuration for CRM organizations."""

    list_display = [
        "name",
        "formatted_team",
        "formatted_status",
        "formatted_industry",
        "last_activity_at",
        "created_at",
        "last_updated_at",
    ]
    list_filter = [
        "team",
        "status",
        "industry",
        "location_state",
        "location_county",
        "location_city",
        "location_zip",
        "created_at",
        "last_updated_at",
    ]
    search_fields = [
        "name",
        "location_city",
        "location_state",
    ]
    ordering = ["name"]
    autocomplete_fields = [
        "team",
        "status",
        "industry",
        "primary_contact",
        "location_city",
        "location_state",
        "location_county",
        "location_zip",
        "tags",
    ]
    filter_horizontal = ["tags"]
    readonly_fields = [
        "id",
        "created_at",
        "last_updated_at",
        "created_by",
    ]

    fieldsets = [
        (
            _("Organization"),
            {
                "classes": ["tab"],
                "fields": [
                    "name",
                    "team",
                    "status",
                    "industry",
                    "primary_contact",
                    "tags",
                    "address_one",
                    "address_two",
                    "location_city",
                    "location_state",
                    "location_county",
                    "location_zip",
                    "last_activity_at",
                    "notes",
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

    @display(description=_("Status"), ordering="status__name")
    def formatted_status(self, obj):
        return getattr(obj.status, "name", "-")

    @display(description=_("Industry"), ordering="industry__name")
    def formatted_industry(self, obj):
        return getattr(obj.industry, "name", "-")
