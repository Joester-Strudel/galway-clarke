# Django Imports
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

# First-Party Imports
from ..inlines import AATTermContributorInline, AATTermSourceInline
from ..models import AATTerm


@admin.register(AATTerm)
class AATTermAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_term_text",
        "formatted_subject",
        "formatted_is_preferred",
        "formatted_term_type",
        "formatted_language_code",
    ]
    list_filter = [
        "is_preferred",
        "term_type",
        "part_of_speech",
        "historic_flag",
        "vernacular",
        "created_at",
    ]
    search_fields = [
        "term_text",
        "display_name",
        "term_id",
        "language_code",
        "qualifier",
        "subject__aat_id",
    ]
    ordering = [
        "term_text",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "last_updated_at",
        "created_by",
    ]

    inlines = [
        AATTermContributorInline,
        AATTermSourceInline,
    ]

    # Fieldsets for better organization
    fieldsets = (
        (
            _("General Information"),
            {
                "classes": ["tab"],
                "fields": [
                    "subject",
                    "term_id",
                    "term_text",
                    "display_name",
                    "is_preferred",
                    "term_type",
                    "part_of_speech",
                    "language_code",
                    "qualifier",
                    "historic_flag",
                    "vernacular",
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

    @display(description="Term", ordering="term_text")
    def formatted_term_text(self, obj):
        value = obj.display_name or obj.term_text
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": value,
                    "size": "medium",
                },
            )
        )

    @display(description="Subject", ordering="subject__aat_id")
    def formatted_subject(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.subject,
                    "size": "small",
                },
            )
        )

    @display(description="Preferred", ordering="is_preferred")
    def formatted_is_preferred(self, obj):
        options = {
            True: {
                "label": "Preferred",
                "icon": "check_circle",
                "color": "green",
            },
            False: {
                "label": "Not preferred",
                "icon": "cancel",
                "color": "slate",
            },
        }

        option = options[obj.is_preferred]

        return mark_safe(
            render_to_string(
                "admin/badge.html",
                {
                    "label": option["label"],
                    "icon": option["icon"],
                    "color": option["color"],
                },
            )
        )

    @display(description="Term Type", ordering="term_type")
    def formatted_term_type(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.term_type or "N/A",
                    "size": "small",
                },
            )
        )

    @display(description="Language", ordering="language_code")
    def formatted_language_code(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.language_code or "N/A",
                    "size": "small",
                },
            )
        )
