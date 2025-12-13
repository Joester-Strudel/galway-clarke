# Django Imports
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from unfold.admin import ModelAdmin, display

# First-Party Imports
from ..models import Individual


@admin.register(Individual)
class IndividualAdmin(ModelAdmin):
    """Admin configuration for CRM individuals."""

    list_display = [
        "full_name",
        "email",
        "phone",
        "formatted_team",
        "formatted_org",
        "primary",
        "created_at",
        "last_updated_at",
    ]
    list_filter = [
        "primary",
        "team",
        "organization",
        "tags",
        "location_state",
        "location_county",
        "location_city",
        "location_zip",
        "created_at",
        "last_updated_at",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
    ]
    ordering = ["-created_at"]
    autocomplete_fields = [
        "team",
        "organization",
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
            _("Individual"),
            {
                "classes": ["tab"],
                "fields": [
                    "team",
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "address_one",
                    "address_two",
                    "location_city",
                    "location_state",
                    "location_county",
                    "location_zip",
                    "organization",
                    "tags",
                    "primary",
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

    @display(description=_("Organization"), ordering="organization__name")
    def formatted_org(self, obj):
        return getattr(obj.organization, "name", "-")
