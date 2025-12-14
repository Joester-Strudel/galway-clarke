# Django Imports
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.utils.dateparse import parse_date

# Standard Library Imports
from urllib.parse import urlencode

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


def _get_filters(request):
    """Extract filter inputs from the request, trimming whitespace."""
    return {
        "filter_name": request.GET.get("filter_name", "").strip(),
        "filter_status": request.GET.get("filter_status", "").strip(),
        "filter_city": request.GET.get("filter_city", "").strip(),
        "filter_state": request.GET.get("filter_state", "").strip(),
        "filter_industry": request.GET.get("filter_industry", "").strip(),
        "filter_primary_contact": request.GET.get("filter_primary_contact", "").strip(),
        "filter_last_activity": request.GET.get("filter_last_activity", "").strip(),
        "filter_tag": request.GET.get("filter_tag", "").strip(),
    }


def _filter_fields(filters):
    """Define filter field metadata for the filter tray UI."""
    return [
        {
            "label": "Name",
            "name": "filter_name",
            "value": filters.get("filter_name", ""),
            "placeholder": "Name contains",
        },
        {
            "label": "Status",
            "name": "filter_status",
            "value": filters.get("filter_status", ""),
            "placeholder": "Status contains",
        },
        {
            "label": "City",
            "name": "filter_city",
            "value": filters.get("filter_city", ""),
            "placeholder": "City contains",
        },
        {
            "label": "State/Region",
            "name": "filter_state",
            "value": filters.get("filter_state", ""),
            "placeholder": "State or region contains",
        },
        {
            "label": "Industry",
            "name": "filter_industry",
            "value": filters.get("filter_industry", ""),
            "placeholder": "Industry contains",
        },
        {
            "label": "Primary Contact",
            "name": "filter_primary_contact",
            "value": filters.get("filter_primary_contact", ""),
            "placeholder": "Name contains",
        },
        {
            "label": "Last Activity",
            "name": "filter_last_activity",
            "value": filters.get("filter_last_activity", ""),
            "placeholder": "YYYY-MM-DD or year",
        },
        {
            "label": "Tag",
            "name": "filter_tag",
            "value": filters.get("filter_tag", ""),
            "placeholder": "Tag contains",
        },
    ]


def _filter_querystring(filters):
    active_filters = {key: value for key, value in filters.items() if value}
    if not active_filters:
        return ""
    return "&" + urlencode(active_filters)


def _get_org_page(request):
    team = _get_active_team(request)
    search_query = request.GET.get("search", "").strip()
    sort_field = request.GET.get("sort", "name")
    sort_direction = request.GET.get("direction", "asc")
    filters = _get_filters(request)

    allowed_sorts = {
        "name": "name",
        "status": "status__name",
        "city": "location_city__name",
        "state": "location_state__abbreviation",
        "industry": "industry__name",
        "primary_contact": "primary_contact__last_name",
        "last_activity": "last_activity_at",
    }

    sort_field = sort_field if sort_field in allowed_sorts else "name"
    sort_direction = "desc" if sort_direction == "desc" else "asc"
    sort_expr = allowed_sorts[sort_field]
    if sort_direction == "desc":
        sort_expr = f"-{sort_expr}"

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

    if search_query:
        qs = qs.filter(name__icontains=search_query)

    if filters["filter_name"]:
        qs = qs.filter(name__icontains=filters["filter_name"])
    if filters["filter_status"]:
        qs = qs.filter(status__name__icontains=filters["filter_status"])
    if filters["filter_city"]:
        qs = qs.filter(location_city__name__icontains=filters["filter_city"])
    if filters["filter_state"]:
        qs = qs.filter(
            Q(location_state__abbreviation__icontains=filters["filter_state"])
            | Q(location_state__name__icontains=filters["filter_state"])
        )
    if filters["filter_industry"]:
        qs = qs.filter(industry__name__icontains=filters["filter_industry"])
    if filters["filter_primary_contact"]:
        qs = qs.filter(
            Q(primary_contact__first_name__icontains=filters["filter_primary_contact"])
            | Q(primary_contact__last_name__icontains=filters["filter_primary_contact"])
        )
    if filters["filter_last_activity"]:
        parsed_date = parse_date(filters["filter_last_activity"])
        if parsed_date:
            qs = qs.filter(last_activity_at__date=parsed_date)
        elif filters["filter_last_activity"].isdigit() and len(filters["filter_last_activity"]) == 4:
            qs = qs.filter(last_activity_at__year=int(filters["filter_last_activity"]))
    if filters["filter_tag"]:
        qs = qs.filter(tags__name__icontains=filters["filter_tag"])

    qs = qs.order_by(sort_expr, "id")
    if filters["filter_tag"]:
        qs = qs.distinct()

    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    filter_fields = _filter_fields(filters)
    filter_querystring = _filter_querystring(filters)
    return page_obj, search_query, sort_field, sort_direction, filters, filter_fields, filter_querystring


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
    page_obj, search_query, sort_field, sort_direction, filters, filter_fields, filter_querystring = _get_org_page(request)
    pagination = _pagination_context(page_obj)
    context = {
        "workspace_template": "cotton/app/gc_crm/pages/index.html",
        "initial_tab": "organizations",
        "search_query": search_query,
        "sort_field": sort_field,
        "sort_direction": sort_direction,
        "filters": filters,
        "filter_fields": filter_fields,
        "filter_querystring": filter_querystring,
        **pagination,
    }

    if request.htmx:
        return render(request, "cotton/app/gc_crm/pages/organizations.html", context)

    return render(request, "cotton/app/index.html", context)
