# Django Imports
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

# First-Party Imports
from ..models import UlanPartOfSpeech


@admin.register(UlanPartOfSpeech)
class UlanPartOfSpeechAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_name",
        "created_at",
    ]
    list_filter = [
        "created_at",
    ]
    search_fields = [
        "name",
    ]
    ordering = [
        "name",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "last_updated_at",
        "created_by",
    ]

    # Fieldsets for better organization
    fieldsets = (
        (
            _("General Information"),
            {
                "classes": ["tab"],
                "fields": [
                    "name",
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
    )

    @display(description="Name", ordering="name")
    def formatted_name(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.name,
                    "size": "large",
                },
            )
        )
