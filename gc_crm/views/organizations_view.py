# Django Imports
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from gc_crm.models import Organization


def _get_active_team(request):
    """
    Determine the active team for this request based on session selection.
    Falls back to the first joined or owned team if none is set.
    """
    if not request.user.is_authenticated:
        return None

    active_id = request.session.get("active_organization_id")
    if active_id:
        team = request.user.organizations.filter(id=active_id).first()
        if team:
            return team

    # Fallbacks
    return request.user.organizations.first() or request.user.owned_organizations.first()


def _get_org_page(request):
    team = _get_active_team(request)

    qs = Organization.objects.select_related(
        "team",
        "status",
        "industry",
        "location_city",
        "location_state",
        "primary_contact",
    ).prefetch_related("tags")

    if team:
        qs = qs.filter(team=team)
    else:
        # If no team context, show nothing for authenticated users.
        qs = qs.none()

    qs = qs.order_by("name")

    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


def _pagination_context(page_obj):
    """Return scalar pagination data for templates/components."""
    page_number = page_obj.number if page_obj else 1
    num_pages = page_obj.paginator.num_pages if page_obj else 1
    total_count = page_obj.paginator.count if page_obj else 0
    has_prev = page_obj.has_previous() if page_obj else False
    has_next = page_obj.has_next() if page_obj else False
    prev_page = page_obj.previous_page_number() if has_prev else None
    next_page = page_obj.next_page_number() if has_next else None
    return {
        "page_obj": page_obj,
        "page_number": page_number,
        "num_pages": num_pages,
        "total_count": total_count,
        "has_prev": has_prev,
        "has_next": has_next,
        "prev_page": prev_page,
        "next_page": next_page,
    }


@login_required
def organizations_view(request):
    """Serve the organizations tab content or full shell."""
    pagination = _pagination_context(_get_org_page(request))
    context = {
        "workspace_template": "cotton/app/gc_crm/pages/index.html",
        "initial_tab": "organizations",
        **pagination,
    }

    if request.htmx:
        return render(request, "cotton/app/gc_crm/pages/organizations.html", context)

    return render(request, "cotton/app/index.html", context)
