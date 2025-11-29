# Django Imports
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

# First-Party Imports
from ..models import AATTermSource


@admin.register(AATTermSource)
class AATTermSourceAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_term",
        "formatted_source_id",
        "formatted_page",
        "formatted_preferred_flag",
    ]
    list_filter = [
        "preferred_flag",
        "created_at",
    ]
    search_fields = [
        "source_id",
        "page",
        "preferred_flag",
        "term__term_text",
        "term__term_id",
    ]
    ordering = [
        "-created_at",
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
                    "term",
                    "source_id",
                    "page",
                    "preferred_flag",
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

    @display(description="Term", ordering="term__term_text")
    def formatted_term(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.term,
                    "size": "medium",
                },
            )
        )

    @display(description="Source ID", ordering="source_id")
    def formatted_source_id(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.source_id,
                    "size": "small",
                },
            )
        )

    @display(description="Page", ordering="page")
    def formatted_page(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.page or "N/A",
                    "size": "small",
                },
            )
        )

    @display(description="Preferred Flag", ordering="preferred_flag")
    def formatted_preferred_flag(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.preferred_flag or "N/A",
                    "size": "small",
                },
            )
        )
