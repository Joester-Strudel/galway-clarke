# Django Imports
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from unfold.admin import ModelAdmin, display

# First-Party Imports
from ..models import ZipCode


@admin.register(ZipCode)
class ZipCodeAdmin(ModelAdmin):
    """Admin configuration for ZIP codes."""

    list_display = [
        "formatted_zip",
        "formatted_plus4",
        "formatted_population",
        "formatted_density",
        "created_at",
        "last_updated_at",
    ]
    list_filter = [
        "states",
        "counties",
        "cities",
        "created_at",
        "last_updated_at",
    ]
    search_fields = [
        "zip_code_five_digit",
        "zip_code_nine_digit",
    ]
    ordering = ["zip_code_five_digit"]
    filter_horizontal = [
        "states",
        "counties",
        "cities",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "last_updated_at",
        "created_by",
    ]

    fieldsets = [
        (
            _("ZIP Code"),
            {
                "classes": ["tab"],
                "fields": [
                    "zip_code_five_digit",
                    "zip_code_nine_digit",
                    "population",
                    "density",
                    "states",
                    "counties",
                    "cities",
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

    @display(description=_("ZIP (5 Digit)"), ordering="zip_code_five_digit")
    def formatted_zip(self, obj):
        return mark_safe(
            render_to_string(
                "cotton/admin/components/text.html",
                {
                    "value": obj.zip_code_five_digit,
                    "size": "medium",
                },
            )
        )

    @display(description=_("ZIP (9 Digit)"), ordering="zip_code_nine_digit")
    def formatted_plus4(self, obj):
        return mark_safe(
            render_to_string(
                "cotton/admin/components/text.html",
                {
                    "value": obj.zip_code_nine_digit or "—",
                    "size": "small",
                },
            )
        )

    @display(description=_("Population"), ordering="population")
    def formatted_population(self, obj):
        return mark_safe(
            render_to_string(
                "cotton/admin/components/text.html",
                {
                    "value": obj.population if obj.population is not None else "—",
                    "size": "small",
                },
            )
        )

    @display(description=_("Density"), ordering="density")
    def formatted_density(self, obj):
        return mark_safe(
            render_to_string(
                "cotton/admin/components/text.html",
                {
                    "value": obj.density if obj.density is not None else "—",
                    "size": "small",
                },
            )
        )
