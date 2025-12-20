# Django Imports
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from unfold.admin import ModelAdmin, display

# First-Party Imports
from ..models import County


@admin.register(County)
class CountyAdmin(ModelAdmin):
    """Admin configuration for counties."""

    list_display = [
        "formatted_name",
        "formatted_fips",
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
        return mark_safe(
            render_to_string(
                "cotton/admin/components/text.html",
                {
                    "value": getattr(obj.state, "name", "—"),
                    "size": "small",
                },
            )
        )

    @display(description=_("County"), ordering="name")
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

    @display(description=_("FIPS"), ordering="fips_code")
    def formatted_fips(self, obj):
        return mark_safe(
            render_to_string(
                "cotton/admin/components/text.html",
                {
                    "value": obj.fips_code or "—",
                    "size": "small",
                },
            )
        )
