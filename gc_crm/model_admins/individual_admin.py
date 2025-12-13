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
        "organization",
        "tags",
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
        "organization",
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
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
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

    @display(description=_("Team"), ordering="organization__account__name")
    def formatted_team(self, obj):
        return getattr(getattr(obj.organization, "account", None), "name", "-")

    @display(description=_("Organization"), ordering="organization__name")
    def formatted_org(self, obj):
        return getattr(obj.organization, "name", "-")
