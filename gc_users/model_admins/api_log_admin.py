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
    list_display_links = []
    list_select_related = True
    list_editable = []
    list_per_page = 50
    list_filter = [
        "api_key",
        "status_code",
    ]
    search_fields = [
        "ip_address__icontains",
        "message__icontains",
    ]
    date_hierarchy = "created_at"
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
    prepopulated_fields = {}
    formfield_overrides = {}
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
    filter_horizontal = []
    filter_vertical = []

    # 3. Inlines
    inlines = []

    # 4. Actions and Behavior
    actions = []
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True
    save_as = True

    # 5. Methods (Unmodified, uses super())
    def save_model(self, request, obj, form, change):
        return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        return super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        return super().delete_queryset(request, queryset)

    def save_formset(self, request, form, formset, change):
        return super().save_formset(request, form, formset, change)

    def get_ordering(self, request):
        return super().get_ordering(request)

    def get_search_results(self, request, queryset, search_term):
        return super().get_search_results(request, queryset, search_term)

    def save_related(self, request, form, formsets, change):
        return super().save_related(request, form, formsets, change)

    def get_autocomplete_fields(self, request):
        return super().get_autocomplete_fields(request)

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj)

    def get_prepopulated_fields(self, request, obj=None):
        return super().get_prepopulated_fields(request, obj)

    def get_list_display(self, request):
        return super().get_list_display(request)

    def get_list_display_links(self, request, list_display):
        return super().get_list_display_links(request, list_display)

    def get_exclude(self, request, obj=None):
        return super().get_exclude(request, obj)

    def get_fields(self, request, obj=None):
        return super().get_fields(request, obj)

    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj)

    def get_list_filter(self, request):
        return super().get_list_filter(request)

    def get_list_select_related(self, request):
        return super().get_list_select_related(request)

    def get_search_fields(self, request):
        return super().get_search_fields(request)

    def get_sortable_by(self, request):
        return super().get_sortable_by(request)

    def get_inline_instances(self, request, obj=None):
        return super().get_inline_instances(request, obj)

    def get_inlines(self, request, obj):
        return super().get_inlines(request, obj)

    def get_urls(self):
        return super().get_urls()

    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj, **kwargs)

    def get_formsets_with_inlines(self, request, obj=None):
        return super().get_formsets_with_inlines(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def get_changelist(self, request, **kwargs):
        return super().get_changelist(request, **kwargs)

    def get_changelist_form(self, request, **kwargs):
        return super().get_changelist_form(request, **kwargs)

    def get_changelist_formset(self, request, **kwargs):
        return super().get_changelist_formset(request, **kwargs)

    def lookup_allowed(self, lookup, value):
        return super().lookup_allowed(lookup, value)

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj)

    def has_module_permission(self, request):
        return super().has_module_permission(request)

    def get_queryset(self, request):
        return super().get_queryset(request)

    def message_user(self, request, message, level=None, extra_tags="", fail_silently=False):
        super().message_user(request, message, level, extra_tags, fail_silently)

    def get_paginator(self, request, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super().get_paginator(request, queryset, per_page, orphans, allow_empty_first_page)

    def response_add(self, request, obj, post_url_continue=None):
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        return super().response_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        return super().response_delete(request, obj_display, obj_id)

    def get_formset_kwargs(self, request, obj, inline, prefix):
        return super().get_formset_kwargs(request, obj, inline, prefix)

    def get_changeform_initial_data(self, request):
        return super().get_changeform_initial_data(request)

    def get_deleted_objects(self, objs, request):
        return super().get_deleted_objects(objs, request)

    def add_view(self, request, form_url="", extra_context=None):
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        return super().change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context)

    def delete_view(self, request, object_id, extra_context=None):
        return super().delete_view(request, object_id, extra_context)

    def history_view(self, request, object_id, extra_context=None):
        return super().history_view(request, object_id, extra_context)

    # 6. Interface Customization
    add_form_template = None
    change_form_template = None
    change_list_template = None
    delete_confirmation_template = None
    delete_selected_confirmation_template = None
    object_history_template = None
    popup_response_template = None

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
        503: {"name": _("Service Unavailable"), "icon": "hourglass-half", "color": "red"},
    }

    @display(description=_("Status"), ordering="status_code")
    def formatted_status_code(self, obj):
        """Render the formatted case status as a styled badge."""
        status_info = self.STATUS_CHOICES.get(
            obj.status_code,
            {"name": _("Unknown"), "icon": "circle", "color": "gray"}
        )

        return mark_safe(
            render_to_string("admin/widgets/badge.html", {
                "label": status_info["name"],
                "icon": status_info["icon"],
                "color": status_info["color"],
            })
        )

    # 7. Media Assets
    class Media:
        css = {}
        js = []
