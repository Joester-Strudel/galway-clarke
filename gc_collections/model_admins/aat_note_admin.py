# Django Imports
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

# First-Party Imports
from ..models import AATNote


@admin.register(AATNote)
class AATNoteAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_subject",
        "formatted_note_language",
        "formatted_note_text",
    ]
    list_filter = [
        "note_language",
        "created_at",
    ]
    search_fields = [
        "note_text",
        "note_language",
        "subject__aat_id",
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
                    "subject",
                    "note_text",
                    "note_language",
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

    @display(description="Subject", ordering="subject__aat_id")
    def formatted_subject(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.subject,
                    "size": "medium",
                },
            )
        )

    @display(description="Language", ordering="note_language")
    def formatted_note_language(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.note_language,
                    "size": "small",
                },
            )
        )

    @display(description="Note Text", ordering="note_text")
    def formatted_note_text(self, obj):
        note_preview = obj.note_text[:75]
        if len(obj.note_text) > 75:
            note_preview = f"{note_preview}..."

        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": note_preview,
                    "size": "small",
                },
            )
        )
