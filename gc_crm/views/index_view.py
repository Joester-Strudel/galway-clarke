# Django Imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from gc_crm.views.organizations_view import _get_org_page


@login_required
def index_view(request):
    """
    Render the CRM contacts page. If this is an HTMX request, return only the
    contacts fragment; otherwise return the full shell.
    """
    page_obj = _get_org_page(request)
    context = {
        "workspace_template": "cotton/app/gc_crm/pages/index.html",
        "initial_tab": "organizations",
        "page_obj": page_obj,
    }

    htmx_context = {"initial_tab": "organizations"}

    if request.htmx:
        return render(request, "cotton/app/gc_crm/pages/index.html", htmx_context)

    return render(request, "cotton/app/index.html", context)
