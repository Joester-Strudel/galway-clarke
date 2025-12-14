# Django Imports
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from gc_crm.models import Organization


def _get_org_page(request):
    team = None
    if request.user.is_authenticated:
        # Prefer a team the user belongs to; fall back to owned teams.
        team = request.user.organizations.first() or request.user.owned_organizations.first()

    qs = Organization.objects.select_related(
        "team",
        "status",
        "industry",
        "location_city",
        "location_state",
        "primary_contact",
    ).prefetch_related("tags")

    if team and not request.user.is_superuser:
        qs = qs.filter(team=team)

    qs = qs.order_by("name")

    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required
def organizations_view(request):
    """Serve the organizations tab content or full shell."""
    page_obj = _get_org_page(request)
    context = {
        "workspace_template": "cotton/app/gc_crm/pages/index.html",
        "initial_tab": "organizations",
        "page_obj": page_obj,
    }

    if request.htmx:
        return render(request, "cotton/app/gc_crm/pages/organizations.html", {"page_obj": page_obj})

    return render(request, "cotton/app/index.html", context)
