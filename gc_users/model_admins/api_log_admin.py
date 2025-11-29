# Django Imports
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Third-Party Imports
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, display

# First-Party Imports
from ..models import ApiLog


@admin.register(ApiLog)
class ApiLogAdmin(SimpleHistoryAdmin, ModelAdmin):
    """Admin configuration for ApiLog."""

    # 1. Basic Configuration
    list_display = [
        "api_key",
        "ip_address",
        "request_path",
        "formatted_status_code",
        "message",
        "created_at",
    ]
    list_select_related = True
    list_per_page = 50
    list_filter = [
        "api_key",
        "status_code",
    ]
    search_fields = [
        "ip_address__icontains",
        "message__icontains",
    ]
    empty_value_display = "-"
    show_facets = True

    # 2. Form Customization
    fieldsets = [
        [
            _("General Information"),
            {
                "classes": ["tab"],
                "fields": [
                    "api_key",
                    "ip_address",
                    "request_path",
                    "status_code",
                    "message",
                ],
            },
        ],
        [
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
        ],
    ]
    autocomplete_fields = [
        "api_key",
    ]
    readonly_fields = [
        "id",
        "status_code",
        "created_at",
        "last_updated_at",
        "created_by",
    ]

    STATUS_CHOICES = {
        200: {"name": _("OK"), "icon": "check_circle", "color": "green"},
        201: {"name": _("Created"), "icon": "library_add", "color": "blue"},
        204: {"name": _("No Content"), "icon": "data_object", "color": "gray"},
        400: {"name": _("Bad Request"), "icon": "heart_broken", "color": "orange"},
        401: {"name": _("Unauthorized"), "icon": "lock", "color": "orange"},
        403: {"name": _("Forbidden"), "icon": "lock", "color": "orange"},
        404: {"name": _("Not Found"), "icon": "travel_explore", "color": "orange"},
        500: {"name": _("Internal Server Error"), "icon": "error", "color": "red"},
        502: {"name": _("Bad Gateway"), "icon": "exchange", "color": "red"},
        503: {
            "name": _("Service Unavailable"),
            "icon": "hourglass-half",
            "color": "red",
        },
    }

    @display(description=_("Status"), ordering="status_code")
    def formatted_status_code(self, obj):
        """Render the formatted case status as a styled badge."""
        status_info = self.STATUS_CHOICES.get(
            obj.status_code, {"name": _("Unknown"), "icon": "circle", "color": "gray"}
        )

        return mark_safe(
            render_to_string(
                "admin/badge.html",
                {
                    "label": status_info["name"],
                    "icon": status_info["icon"],
                    "color": status_info["color"],
                },
            )
        )
