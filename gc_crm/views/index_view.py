# Django Imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from gc_crm.views.organizations_view import _get_org_page, _pagination_context


@login_required
def index_view(request):
    """
    Render the CRM contacts page. If this is an HTMX request, return only the
    contacts fragment; otherwise return the full shell.
    """
    page_obj, search_query, sort_field, sort_direction = _get_org_page(request)
    pagination = _pagination_context(page_obj)
    context = {
        "workspace_template": "cotton/app/gc_crm/pages/index.html",
        "initial_tab": "organizations",
        "search_query": search_query,
        "sort_field": sort_field,
        "sort_direction": sort_direction,
        **pagination,
    }

    htmx_context = {
        "initial_tab": "organizations",
        "search_query": search_query,
        "sort_field": sort_field,
        "sort_direction": sort_direction,
        **pagination,
    }

    if request.htmx:
        return render(request, "cotton/app/gc_crm/pages/index.html", htmx_context)

    return render(request, "cotton/app/index.html", context)
