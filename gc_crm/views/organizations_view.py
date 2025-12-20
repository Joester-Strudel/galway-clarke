# Django Imports
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.dateparse import parse_date
from django.urls import reverse

# Standard Library Imports
import uuid
from urllib.parse import urlencode, urlsplit

from gc_crm.models import Organization, Status, Tag, Industry, Individual
from gc_geography.models import City, State, County, ZipCode


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

    hx_target = request.headers.get("HX-Target")
    if request.htmx and hx_target == "htmx_workspace":
        # Navbar click: return full CRM shell so header/tabs stay visible
        return render(request, "cotton/app/gc_crm/pages/index.html", context)
    if request.htmx:
        return render(request, "cotton/app/gc_crm/pages/organizations.html", context)

    return render(request, "cotton/app/index.html", context)


@login_required
def organization_drawer_view(request, org_id):
    """Return the organization drawer for view/edit, and out-of-band row swap."""
    team = _get_active_team(request)
    organization = (
        Organization.objects.filter(id=org_id, team=team)
        .prefetch_related("tags")
        .select_related("status", "industry", "location_city", "location_state", "location_county", "location_zip", "primary_contact")
        .first()
    )
    if not organization:
        return HttpResponseBadRequest("Organization not found")

    statuses = Status.objects.filter(team=team).order_by("name") if team else Status.objects.none()
    tags = Tag.objects.filter(team=team).order_by("name") if team else Tag.objects.none()
    industries = Industry.objects.filter(team=team).order_by("name") if team else Industry.objects.none()
    individuals = Individual.objects.filter(team=team).order_by("last_name", "first_name") if team else Individual.objects.none()
    active_tab = request.POST.get("active_tab", request.GET.get("active_tab", "general"))
    refresh_table = False

    error = None
    success = None
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        status_id = request.POST.get("status")
        tag_ids = request.POST.getlist("tags")
        notes = request.POST.get("notes", "")
        industry_id = request.POST.get("industry")
        primary_contact_id = request.POST.get("primary_contact")
        address_one = request.POST.get("address_one", "").strip()
        address_two = request.POST.get("address_two", "").strip()
        city_id = request.POST.get("location_city")
        state_id = request.POST.get("location_state")
        county_id = request.POST.get("location_county")
        zip_id = request.POST.get("location_zip")

        if not name:
            error = "Name is required."
        else:
            organization.name = name
            if status_id:
                status = statuses.filter(id=status_id).first()
                organization.status = status
            else:
                organization.status = None
            organization.industry = industries.filter(id=industry_id).first() if industry_id else None
            organization.primary_contact = individuals.filter(id=primary_contact_id).first() if primary_contact_id else None
            organization.address_one = address_one
            organization.address_two = address_two
            organization.location_city = cities.filter(id=city_id).first() if city_id else None
            organization.location_state = states.filter(id=state_id).first() if state_id else None
            organization.location_county = counties.filter(id=county_id).first() if county_id else None
            organization.location_zip = zip_codes.filter(id=zip_id).first() if zip_id else None
            organization.notes = notes

            valid_tags = tags.filter(id__in=tag_ids)
            organization.save()
            organization.tags.set(valid_tags)
            # Refresh from DB for accurate related fields in row partial.
            organization.refresh_from_db()
            success = "Saved changes."
            refresh_table = True

    selected_tag_ids = set(organization.tags.values_list("id", flat=True))
    selected_tags = list(organization.tags.all())
    status_initial = []
    if organization.status:
        status_initial = [
            {
                "value": str(organization.status_id),
                "label": organization.status.name,
                "color": organization.status.color or "gray",
            }
        ]
    tag_initial = [
        {"value": str(tag.id), "label": tag.name, "color": tag.color or "gray"} for tag in selected_tags
    ]
    industry_initial = []
    if organization.industry:
        industry_initial = [
            {
                "value": str(organization.industry_id),
                "label": organization.industry.name,
                "color": organization.industry.color or "gray",
            }
        ]
    primary_contact_initial = []
    if organization.primary_contact:
        primary_contact_initial = [
            {
                "value": str(organization.primary_contact_id),
                "label": f"{organization.primary_contact.first_name} {organization.primary_contact.last_name}".strip()
                or organization.primary_contact.email
                or "Unnamed",
                "color": "gray",
            }
        ]
    city_initial = []
    if organization.location_city:
        city_initial = [
            {
                "value": str(organization.location_city_id),
                "label": f"{organization.location_city.name}{' (' + (organization.location_city.state.abbreviation or organization.location_city.state.name) + ')' if organization.location_city.state else ''}",
                "color": "gray",
            }
        ]
    state_initial = []
    if organization.location_state:
        state_initial = [
            {
                "value": str(organization.location_state_id),
                "label": organization.location_state.abbreviation or organization.location_state.name,
                "color": "gray",
            }
        ]
    county_initial = []
    if organization.location_county:
        county_initial = [{"value": str(organization.location_county_id), "label": organization.location_county.name, "color": "gray"}]
    zip_initial = []
    if organization.location_zip:
        zip_initial = [{"value": str(organization.location_zip_id), "label": organization.location_zip.zip_code_five_digit, "color": "gray"}]
    select_options = {
        "industries": [{"value": "", "label": "Select industry"}]
        + [{"value": str(ind.id), "label": ind.name} for ind in industries],
        "individuals": [{"value": "", "label": "Select primary contact"}]
        + [
            {
                "value": str(person.id),
                "label": (f"{person.first_name} {person.last_name}".strip() or person.email or "Unnamed").strip(),
            }
            for person in individuals
        ],
    }

    context = {
        "organization": organization,
        "statuses": statuses,
        "tags": tags,
        "industries": industries,
        "individuals": individuals,
        "selected_tag_ids": selected_tag_ids,
        "selected_tags": selected_tags,
        "status_initial": status_initial,
        "tag_initial": tag_initial,
        "industry_initial": industry_initial,
        "primary_contact_initial": primary_contact_initial,
        "city_initial": city_initial,
        "state_initial": state_initial,
        "county_initial": county_initial,
        "zip_initial": zip_initial,
        "select_options": select_options,
        "error": error,
        "success": success,
        "active_tab": active_tab,
        "is_new": False,
        "refresh_table": refresh_table,
        "list_refresh_url": _current_list_url(request),
    }
    return render(request, "cotton/app/gc_crm/partials/organization_drawer.html", context)


@login_required
def organization_create_view(request):
    """Render and handle the add-organization drawer."""
    team = _get_active_team(request)
    if not team:
        return HttpResponseBadRequest("Team context not found")

    organization = Organization(id=uuid.uuid4(), team=team)
    statuses = Status.objects.filter(team=team).order_by("name")
    tags = Tag.objects.filter(team=team).order_by("name")
    industries = Industry.objects.filter(team=team).order_by("name")
    individuals = Individual.objects.filter(team=team).order_by("last_name", "first_name")
    active_tab = request.POST.get("active_tab", request.GET.get("active_tab", "general"))
    refresh_table = False

    error = None
    success = None
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        status_id = request.POST.get("status")
        tag_ids = request.POST.getlist("tags")
        notes = request.POST.get("notes", "")
        industry_id = request.POST.get("industry")
        primary_contact_id = request.POST.get("primary_contact")
        address_one = request.POST.get("address_one", "").strip()
        address_two = request.POST.get("address_two", "").strip()
        city_id = request.POST.get("location_city")
        state_id = request.POST.get("location_state")
        county_id = request.POST.get("location_county")
        zip_id = request.POST.get("location_zip")

        if not name:
            error = "Name is required."
        else:
            organization.name = name
            organization.status = statuses.filter(id=status_id).first() if status_id else None
            organization.industry = industries.filter(id=industry_id).first() if industry_id else None
            organization.primary_contact = individuals.filter(id=primary_contact_id).first() if primary_contact_id else None
            organization.address_one = address_one
            organization.address_two = address_two
            organization.location_city = cities.filter(id=city_id).first() if city_id else None
            organization.location_state = states.filter(id=state_id).first() if state_id else None
            organization.location_county = counties.filter(id=county_id).first() if county_id else None
            organization.location_zip = zip_codes.filter(id=zip_id).first() if zip_id else None
            organization.notes = notes
            organization.save()
            valid_tags = tags.filter(id__in=tag_ids)
            organization.tags.set(valid_tags)
            organization.refresh_from_db()
            success = "Organization created."
            refresh_table = True

    selected_tag_ids = set(organization.tags.values_list("id", flat=True))
    selected_tags = list(organization.tags.all())
    status_initial = []
    if organization.status:
        status_initial = [
            {
                "value": str(organization.status_id),
                "label": organization.status.name,
                "color": organization.status.color or "gray",
            }
        ]
    tag_initial = [
        {"value": str(tag.id), "label": tag.name, "color": tag.color or "gray"} for tag in selected_tags
    ]
    industry_initial = []
    if organization.industry:
        industry_initial = [
            {
                "value": str(organization.industry_id),
                "label": organization.industry.name,
                "color": organization.industry.color or "gray",
            }
        ]
    primary_contact_initial = []
    if organization.primary_contact:
        primary_contact_initial = [
            {
                "value": str(organization.primary_contact_id),
                "label": f"{organization.primary_contact.first_name} {organization.primary_contact.last_name}".strip()
                or organization.primary_contact.email
                or "Unnamed",
                "color": "gray",
            }
        ]
    city_initial = []
    if organization.location_city:
        city_initial = [
            {
                "value": str(organization.location_city_id),
                "label": f"{organization.location_city.name}{' (' + (organization.location_city.state.abbreviation or organization.location_city.state.name) + ')' if organization.location_city.state else ''}",
                "color": "gray",
            }
        ]
    state_initial = []
    if organization.location_state:
        state_initial = [
            {
                "value": str(organization.location_state_id),
                "label": organization.location_state.abbreviation or organization.location_state.name,
                "color": "gray",
            }
        ]
    county_initial = []
    if organization.location_county:
        county_initial = [{"value": str(organization.location_county_id), "label": organization.location_county.name, "color": "gray"}]
    zip_initial = []
    if organization.location_zip:
        zip_initial = [{"value": str(organization.location_zip_id), "label": organization.location_zip.zip_code_five_digit, "color": "gray"}]
    select_options = {
        "industries": [{"value": "", "label": "Select industry"}]
        + [{"value": str(ind.id), "label": ind.name} for ind in industries],
        "individuals": [{"value": "", "label": "Select primary contact"}]
        + [
            {
                "value": str(person.id),
                "label": (f"{person.first_name} {person.last_name}".strip() or person.email or "Unnamed").strip(),
            }
            for person in individuals
        ],
    }

    context = {
        "organization": organization,
        "statuses": statuses,
        "tags": tags,
        "industries": industries,
        "individuals": individuals,
        "selected_tag_ids": selected_tag_ids,
        "selected_tags": selected_tags,
        "status_initial": status_initial,
        "tag_initial": tag_initial,
        "industry_initial": industry_initial,
        "primary_contact_initial": primary_contact_initial,
        "city_initial": city_initial,
        "state_initial": state_initial,
        "county_initial": county_initial,
        "zip_initial": zip_initial,
        "select_options": select_options,
        "error": error,
        "success": success,
        "active_tab": active_tab,
        "is_new": True,
        "refresh_table": refresh_table,
        "list_refresh_url": _current_list_url(request),
    }
    return render(request, "cotton/app/gc_crm/partials/organization_drawer.html", context)


def _current_list_url(request):
    """Resolve current list URL (with querystring) for refreshing the table."""
    hx_current = request.headers.get("HX-Current-URL") or ""
    if hx_current:
        parts = urlsplit(hx_current)
        path = parts.path or reverse("crm-organizations")
        query = f"?{parts.query}" if parts.query else ""
        return f"{path}{query}"
    return reverse("crm-organizations")


@login_required
def organization_delete_view(request, org_id):
    """Delete an organization and return a simple acknowledgement."""
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    team = _get_active_team(request)
    organization = Organization.objects.filter(id=org_id, team=team).first()
    if not organization:
        return HttpResponseBadRequest("Organization not found")

    organization.delete()
    return HttpResponse("Deleted")
