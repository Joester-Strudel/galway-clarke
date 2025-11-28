# Django Imports
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin


class ApiRouteAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "name",
    ]
    search_fields = [
        "name",
    ]
    readonly_fields = [
        "id",
        "created",
        "last_updated",
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
                    "created",
                    "last_updated",
                ],
            },
        ),
    )