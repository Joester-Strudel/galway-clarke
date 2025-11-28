# Django Imports
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

# Third-Party Imports
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin

from ..models import ApiRoute


@admin.register(ApiRoute)
class ApiRouteAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "name",
        "created_at",
    ]
    search_fields = [
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
