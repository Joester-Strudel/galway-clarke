# Django Imports
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

# First-Party Imports
from ..models import UlanBiography


@admin.register(UlanBiography)
class UlanBiographyAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_subject",
        "formatted_biography_id",
        "formatted_is_preferred",
        "formatted_birth_place",
        "formatted_death_place",
    ]
    list_filter = [
        "is_preferred",
        "created_at",
    ]
    search_fields = [
        "biography_id",
        "biography_text",
        "subject__ulan_id",
        "birth_place",
        "death_place",
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
                    "biography_id",
                    "biography_text",
                    "birth_place",
                    "birth_tgn_id",
                    "birth_date",
                    "death_place",
                    "death_tgn_id",
                    "death_date",
                    "sex",
                    "contributor_id",
                    "is_preferred",
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

    @display(description="Subject", ordering="subject__ulan_id")
    def formatted_subject(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.subject, "size": "medium"},
            )
        )

    @display(description="Biography ID", ordering="biography_id")
    def formatted_biography_id(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.biography_id, "size": "small"},
            )
        )

    @display(description="Preferred", ordering="is_preferred")
    def formatted_is_preferred(self, obj):
        options = {
            True: {"label": "Preferred", "icon": "check_circle", "color": "green"},
            False: {"label": "Not preferred", "icon": "cancel", "color": "slate"},
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

    @display(description="Birth Place", ordering="birth_place")
    def formatted_birth_place(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.birth_place or "N/A", "size": "small"},
            )
        )

    @display(description="Death Place", ordering="death_place")
    def formatted_death_place(self, obj):
        return mark_safe(
            render_to_string(
                "admin/text.html",
                {"value": obj.death_place or "N/A", "size": "small"},
            )
        )
