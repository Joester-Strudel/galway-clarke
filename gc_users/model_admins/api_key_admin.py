# Django Imports
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin, display
from simple_history.admin import SimpleHistoryAdmin

from ..models import ApiKey



@admin.register(ApiKey)
class ApiKeyAdmin(SimpleHistoryAdmin, ModelAdmin):
    # List Display
    list_display = [
        "formatted_name",
        "formatted_active",
        "formatted_route_count",
        "formatted_start_date",
        "formatted_end_date",
        "formatted_ip_address",
    ]
    list_filter = [
        "active",
        "start_date",
        "end_date",
        "created_at",
    ]
    search_fields = [
        "name",
        "key",
        "ip_address",
    ]
    ordering = [
        "-created_at",
    ]
    readonly_fields = [
        "id",
        "key",
        "created_at",
        "last_updated_at",
        "created_by",
        "masked_key",
    ]

    # Custom method to display a masked API key for security
    def masked_key(self, obj):
        return format_html("<code>{}********</code>", obj.key[:8]) if obj.key else "No Key"

    masked_key.short_description = "API Key"

    # Fieldsets for better organization
    fieldsets = (
        (
            _("General Information"),
            {
                "classes": ["tab"],
                "fields": [
                    "name",
                    "ip_address",
                    "key",
                    "active",
                    "start_date",
                    "end_date",
                    "routes",
                    "masked_key",
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

    formfield_overrides = {
        models.ManyToManyField: {
            "widget": CheckboxSelectMultiple,
        },
    }

    @display(description="Name", ordering="name")
    def formatted_name(self, obj):
        return mark_safe(
            render_to_string(
                "admin/widgets/text.html",
                {
                    "value": obj.name,
                    "size": "large",
                }
            )
        )
    
    @display(description="Start Date", ordering="start_date")
    def formatted_start_date(self, obj):
        return mark_safe(
            render_to_string(
                "gc_core/admin/widgets/text.html",
                {
                    "value": obj.start_date,
                    "size": "small",
                }
            )
        )
    
    @display(description="End Date", ordering="end_date")
    def formatted_end_date(self, obj):
        return mark_safe(
            render_to_string(
                "gc_core/admin/widgets/text.html",
                {
                    "value": obj.end_date,
                    "size": "small",
                }
            )
        )

    @display(description="Status", ordering="active")
    def formatted_active(self, obj):
        display_options = {
            True: {
                "label": "Active",
                "icon": "radio_button_checked",
                "color": "green",
            },
            False: {
                "label": "Inactive",
                "icon": "radio_button_unchecked",
                "color": "red",
            }        
        }

        option = display_options.get(obj.active, display_options[False])  # Default to "Inactive"

        return mark_safe(
            render_to_string(
                "gc_core/admin/widgets/badge.html",
                {
                    "label": option["label"],
                    "icon": option["icon"],
                    "color": option["color"]
                }
            )
        )
    
    @display(description="IP Address", ordering="ip_address")
    def formatted_ip_address(self, obj):
        return mark_safe(
            render_to_string(
                "gc_core/admin/widgets/text.html",
                {
                    "value": obj.ip_address,
                    "size": "small",
                }
            )
        )
    
    @display(description="Routes")
    def formatted_route_count(self, obj):
        route_count = obj.routes.count()

        # Determine label and color based on route count
        if route_count == 0:
            label = "No routes"
            color = "slate"
        elif route_count == 1:
            label = "1 route"
            color = "purple"
        else:
            label = f"{route_count} routes"
            color = "purple"

        return mark_safe(
            render_to_string(
                "gc_core/admin/widgets/badge.html",
                {
                    "label": label,
                    "icon": "route",
                    "color": color,
                }
            )
        )
