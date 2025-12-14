from django.shortcuts import render

from gc_crm.models import Individual, Organization
from gc_crm.views.organizations_view import _get_active_team


def _dashboard_stats(request):
    """Return dashboard summary stats scoped to the active team."""
    team = _get_active_team(request)
    return {
        "organization_count": Organization.objects.filter(team=team).count()
        if team
        else 0,
        "contact_count": Individual.objects.filter(team=team).count() if team else 0,
    }


def get_dashboard_index(request):
    """
    Render the dashboard page. If this is an HTMX request, return only the
    dashboard fragment; otherwise return the full shell.
    """
    stats = _dashboard_stats(request)

    if request.headers.get("HX-Request") == "true":
        return render(request, "cotton/app/gc_dashboard/pages/index.html", stats)

    # For non-HTMX requests, render the full shell with the dashboard content preloaded.
    return render(
        request,
        "cotton/app/index.html",
        {
            "workspace_template": "cotton/app/gc_dashboard/pages/index.html",
            **stats,
        },
    )
