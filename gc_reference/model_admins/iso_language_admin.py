# Django Imports
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

# First-Party Imports
from ..models import IsoLanguage


@admin.register(IsoLanguage)
class IsoLanguageAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_name",
        "formatted_iso_639_1",
        "formatted_iso_639_2",
        "formatted_iso_639_3",
        "formatted_iso_639_5",
        "formatted_scope",
        "formatted_type",
        "formatted_getty_language_code",
        "created_at",
    ]
    list_filter = [
        "iso_language_scope",
        "iso_language_type",
        "created_at",
    ]
    search_fields = [
        "name",
        "iso_set_639_1_code",
        "iso_set_639_2_code",
        "iso_set_639_3_code",
        "iso_set_639_5_code",
        "iso_language_scope__name",
        "iso_language_type__name",
        "getty_language_code",
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
                    "iso_set_639_1_code",
                    "iso_set_639_2_code",
                    "iso_set_639_3_code",
                    "iso_set_639_5_code",
                    "getty_language_code",
                    "iso_language_scope",
                    "iso_language_type",
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

    @display(description="ISO 639-1", ordering="iso_set_639_1_code")
    def formatted_iso_639_1(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.iso_set_639_1_code or "N/A",
                    "size": "small",
                },
            )
        )

    @display(description="ISO 639-2", ordering="iso_set_639_2_code")
    def formatted_iso_639_2(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.iso_set_639_2_code or "N/A",
                    "size": "small",
                },
            )
        )

    @display(description="ISO 639-3", ordering="iso_set_639_3_code")
    def formatted_iso_639_3(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.iso_set_639_3_code or "N/A",
                    "size": "small",
                },
            )
        )

    @display(description="ISO 639-5", ordering="iso_set_639_5_code")
    def formatted_iso_639_5(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.iso_set_639_5_code or "N/A",
                    "size": "small",
                },
            )
        )

    @display(description="Getty Code", ordering="getty_language_code")
    def formatted_getty_language_code(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.getty_language_code or "N/A",
                    "size": "small",
                },
            )
        )

    @display(description="Scope", ordering="iso_language_scope__name")
    def formatted_scope(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.iso_language_scope or "N/A",
                    "size": "small",
                },
            )
        )

    @display(description="Type", ordering="iso_language_type__name")
    def formatted_type(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {
                    "value": obj.iso_language_type or "N/A",
                    "size": "small",
                },
            )
        )
