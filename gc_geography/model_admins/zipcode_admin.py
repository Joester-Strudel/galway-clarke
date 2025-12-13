# Django Imports
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from unfold.admin import ModelAdmin, display

# First-Party Imports
from ..models import ZipCode


@admin.register(ZipCode)
class ZipCodeAdmin(ModelAdmin):
    """Admin configuration for ZIP codes."""

    list_display = [
        "zip_code_five_digit",
        "zip_code_nine_digit",
        "population",
        "density",
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
