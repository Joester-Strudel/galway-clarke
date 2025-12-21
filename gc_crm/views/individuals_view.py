# Standard Library Imports
import uuid
from urllib.parse import urlencode

# Django Imports
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

# First-Party Imports
from gc_crm.models import Individual, Tag, Organization
from gc_crm.views.organizations_view import (
    _get_active_team,
    _pagination_context,
    _current_list_url,
)
from gc_geography.models import City, State, County, ZipCode


def _get_filters(request):
    """Extract filter inputs for individuals."""
    return {
        "filter_name": request.GET.get("filter_name", "").strip(),
        "filter_email": request.GET.get("filter_email", "").strip(),
        "filter_phone": request.GET.get("filter_phone", "").strip(),
        "filter_org": request.GET.get("filter_org", "").strip(),
        "filter_city": request.GET.get("filter_city", "").strip(),
        "filter_state": request.GET.get("filter_state", "").strip(),
        "filter_tag": request.GET.get("filter_tag", "").strip(),
        "filter_primary": request.GET.get("filter_primary", "").strip(),
    }


def _filter_fields(filters):
    """Define filter metadata for the filter tray."""
    return [
        {
            "label": "Name",
            "name": "filter_name",
            "value": filters.get("filter_name", ""),
            "placeholder": "First or last name contains",
        },
        {
            "label": "Email",
            "name": "filter_email",
            "value": filters.get("filter_email", ""),
            "placeholder": "Email contains",
        },
        {
            "label": "Phone",
            "name": "filter_phone",
            "value": filters.get("filter_phone", ""),
            "placeholder": "Phone contains",
        },
        {
            "label": "Organization",
            "name": "filter_org",
            "value": filters.get("filter_org", ""),
            "placeholder": "Organization name contains",
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
            "label": "Tag",
            "name": "filter_tag",
            "value": filters.get("filter_tag", ""),
            "placeholder": "Tag contains",
        },
        {
            "label": "Primary",
            "name": "filter_primary",
            "value": filters.get("filter_primary", ""),
            "placeholder": "Yes / No",
        },
    ]


def _filter_querystring(filters):
    active_filters = {key: value for key, value in filters.items() if value}
    if not active_filters:
        return ""
    return "&" + urlencode(active_filters)


def _get_individual_page(request):
    team = _get_active_team(request)
    search_query = request.GET.get("search", "").strip()
    sort_field = request.GET.get("sort", "name")
    sort_direction = request.GET.get("direction", "asc")
    filters = _get_filters(request)

    allowed_sorts = {
        "name": ("last_name", "first_name"),
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "email",
        "phone": "phone",
        "organization": "organization__name",
        "city": "location_city__name",
        "state": "location_state__abbreviation",
        "primary": "primary",
    }

    sort_field = sort_field if sort_field in allowed_sorts else "name"
    sort_direction = "desc" if sort_direction == "desc" else "asc"
    sort_expr = allowed_sorts[sort_field]
    sort_list = list(sort_expr) if isinstance(sort_expr, (list, tuple)) else [sort_expr]
    if sort_direction == "desc":
        sort_list = [f"-{expr}" for expr in sort_list]
    sort_list.append("id")

    qs = Individual.objects.select_related(
        "team",
        "organization",
        "location_city",
        "location_state",
        "location_county",
        "location_zip",
    ).prefetch_related("tags")

    if team:
        qs = qs.filter(team=team)
    else:
        qs = qs.none()

    if search_query:
        qs = qs.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(organization__name__icontains=search_query)
        )

    if filters["filter_name"]:
        qs = qs.filter(
            Q(first_name__icontains=filters["filter_name"])
            | Q(last_name__icontains=filters["filter_name"])
        )
    if filters["filter_email"]:
        qs = qs.filter(email__icontains=filters["filter_email"])
    if filters["filter_phone"]:
        qs = qs.filter(phone__icontains=filters["filter_phone"])
    if filters["filter_org"]:
        qs = qs.filter(organization__name__icontains=filters["filter_org"])
    if filters["filter_city"]:
        qs = qs.filter(location_city__name__icontains=filters["filter_city"])
    if filters["filter_state"]:
        qs = qs.filter(
            Q(location_state__abbreviation__icontains=filters["filter_state"])
            | Q(location_state__name__icontains=filters["filter_state"])
        )
    if filters["filter_tag"]:
        qs = qs.filter(tags__name__icontains=filters["filter_tag"])
    if filters["filter_primary"]:
        val = filters["filter_primary"].lower()
        if val in ("true", "yes", "y", "1", "primary"):
            qs = qs.filter(primary=True)
        elif val in ("false", "no", "0", "n"):
            qs = qs.filter(primary=False)

    qs = qs.order_by(*sort_list)
    if filters["filter_tag"]:
        qs = qs.distinct()

    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    filter_fields = _filter_fields(filters)
    filter_querystring = _filter_querystring(filters)

    return (
        page_obj,
        search_query,
        sort_field,
        sort_direction,
        filters,
        filter_fields,
        filter_querystring,
    )


@login_required
def individuals_view(request):
    """Serve the individuals tab content or full shell."""
    (
        page_obj,
        search_query,
        sort_field,
        sort_direction,
        filters,
        filter_fields,
        filter_querystring,
    ) = _get_individual_page(request)
    pagination = _pagination_context(page_obj)
    context = {
        "workspace_template": "cotton/app/gc_crm/pages/index.html",
        "initial_tab": "individuals",
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
        return render(request, "cotton/app/gc_crm/pages/index.html", context)
    if request.htmx:
        return render(request, "cotton/app/gc_crm/pages/individuals.html", context)

    return render(request, "cotton/app/index.html", context)


@login_required
def individual_drawer_view(request, individual_id):
    """
    Return the individual drawer for view/edit, with OOB row swap.
    """
    team = _get_active_team(request)
    individual = (
        Individual.objects.filter(id=individual_id, team=team)
        .prefetch_related("tags")
        .select_related(
            "organization",
            "location_city",
            "location_state",
            "location_county",
            "location_zip",
        )
        .first()
    )
    if not individual:
        return HttpResponseBadRequest("Individual not found")

    tags = Tag.objects.filter(team=team).order_by("name") if team else Tag.objects.none()
    organizations = (
        Organization.objects.filter(team=team).order_by("name")
        if team
        else Organization.objects.none()
    )
    cities = City.objects.select_related("state")
    states = State.objects.all()
    counties = County.objects.select_related("state")
    zip_codes = ZipCode.objects.all()
    active_tab = request.POST.get(
        "active_tab", request.GET.get("active_tab", "general")
    )
    refresh_table = False
    save_url = reverse("crm-individual-edit", args=[individual.id])
    delete_url = reverse("crm-individual-delete", args=[individual.id])

    error = None
    success = None
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        organization_id = request.POST.get("organization")
        tag_ids = request.POST.getlist("tags")
        primary = request.POST.get("primary") in ["on", "true", "1", "yes"]
        notes = request.POST.get("notes", "")
        address_one = request.POST.get("address_one", "").strip()
        address_two = request.POST.get("address_two", "").strip()
        city_id = request.POST.get("location_city")
        state_id = request.POST.get("location_state")
        county_id = request.POST.get("location_county")
        zip_id = request.POST.get("location_zip")

        if not (first_name or last_name or email or phone):
            error = "Provide at least a name, email, or phone."
        else:
            individual.first_name = first_name
            individual.last_name = last_name
            individual.email = email or None
            individual.phone = phone or None
            individual.organization = (
                organizations.filter(id=organization_id).first()
                if organization_id
                else None
            )
            individual.primary = primary
            individual.address_one = address_one
            individual.address_two = address_two
            individual.location_city = (
                cities.filter(id=city_id).first() if city_id else None
            )
            individual.location_state = (
                states.filter(id=state_id).first() if state_id else None
            )
            individual.location_county = (
                counties.filter(id=county_id).first() if county_id else None
            )
            individual.location_zip = (
                zip_codes.filter(id=zip_id).first() if zip_id else None
            )
            individual.notes = notes

            valid_tags = tags.filter(id__in=tag_ids)
            individual.save()
            individual.tags.set(valid_tags)
            individual.refresh_from_db()
            success = "Saved changes."
            refresh_table = True

    selected_tags = list(individual.tags.all())
    tag_initial = [
        {"value": str(tag.id), "label": tag.name, "color": tag.color or "gray"}
        for tag in selected_tags
    ]
    organization_initial = []
    if individual.organization:
        organization_initial = [
            {
                "value": str(individual.organization_id),
                "label": individual.organization.name,
                "color": "gray",
            }
        ]
    city_initial = []
    if individual.location_city:
        city_initial = [
            {
                "value": str(individual.location_city_id),
                "label": f"{individual.location_city.name}{' (' + (individual.location_city.state.abbreviation or individual.location_city.state.name) + ')' if individual.location_city.state else ''}",
                "color": "gray",
            }
        ]
    state_initial = []
    if individual.location_state:
        state_initial = [
            {
                "value": str(individual.location_state_id),
                "label": individual.location_state.name,
                "color": "gray",
            }
        ]
    county_initial = []
    if individual.location_county:
        county_label_state = ""
        if individual.location_county.state:
            county_label_state = (
                individual.location_county.state.abbreviation
                or individual.location_county.state.name
                or ""
            )
        county_label = individual.location_county.name
        if county_label_state:
            county_label = f"{county_label} ({county_label_state})"
        county_initial = [
            {
                "value": str(individual.location_county_id),
                "label": county_label,
                "color": "gray",
            }
        ]
    zip_initial = []
    if individual.location_zip:
        zip_initial = [
            {
                "value": str(individual.location_zip_id),
                "label": individual.location_zip.zip_code_five_digit,
                "color": "gray",
            }
        ]

    context = {
        "individual": individual,
        "tags": tags,
        "organizations": organizations,
        "tag_initial": tag_initial,
        "organization_initial": organization_initial,
        "city_initial": city_initial,
        "state_initial": state_initial,
        "county_initial": county_initial,
        "zip_initial": zip_initial,
        "error": error,
        "success": success,
        "active_tab": active_tab,
        "is_new": False,
        "refresh_table": refresh_table,
        "list_refresh_url": _current_list_url(request, "crm-individuals"),
        "save_url": save_url,
        "delete_url": delete_url,
        "edit_url": save_url,
    }
    return render(
        request, "cotton/app/gc_crm/partials/individual_drawer.html", context
    )


@login_required
def individual_create_view(request):
    """Render and handle the add-individual drawer."""
    team = _get_active_team(request)
    if not team:
        return HttpResponseBadRequest("Team context not found")

    individual = Individual(id=uuid.uuid4(), team=team)
    tags = Tag.objects.filter(team=team).order_by("name")
    organizations = Organization.objects.filter(team=team).order_by("name")
    cities = City.objects.select_related("state")
    states = State.objects.all()
    counties = County.objects.select_related("state")
    zip_codes = ZipCode.objects.all()
    active_tab = request.POST.get(
        "active_tab", request.GET.get("active_tab", "general")
    )
    refresh_table = False
    is_new = True
    save_url = reverse("crm-individual-create")
    delete_url = ""
    edit_url = ""

    error = None
    success = None
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        organization_id = request.POST.get("organization")
        tag_ids = request.POST.getlist("tags")
        primary = request.POST.get("primary") in ["on", "true", "1", "yes"]
        notes = request.POST.get("notes", "")
        address_one = request.POST.get("address_one", "").strip()
        address_two = request.POST.get("address_two", "").strip()
        city_id = request.POST.get("location_city")
        state_id = request.POST.get("location_state")
        county_id = request.POST.get("location_county")
        zip_id = request.POST.get("location_zip")

        if not (first_name or last_name or email or phone):
            error = "Provide at least a name, email, or phone."
        else:
            individual.first_name = first_name
            individual.last_name = last_name
            individual.email = email or None
            individual.phone = phone or None
            individual.organization = (
                organizations.filter(id=organization_id).first()
                if organization_id
                else None
            )
            individual.primary = primary
            individual.address_one = address_one
            individual.address_two = address_two
            individual.location_city = (
                cities.filter(id=city_id).first() if city_id else None
            )
            individual.location_state = (
                states.filter(id=state_id).first() if state_id else None
            )
            individual.location_county = (
                counties.filter(id=county_id).first() if county_id else None
            )
            individual.location_zip = (
                zip_codes.filter(id=zip_id).first() if zip_id else None
            )
            individual.notes = notes
            individual.save()

            valid_tags = tags.filter(id__in=tag_ids)
            individual.tags.set(valid_tags)
            individual.refresh_from_db()
            success = "Individual created."
            refresh_table = True
            is_new = False
            edit_url = reverse("crm-individual-edit", args=[individual.id])
            save_url = edit_url
            delete_url = reverse("crm-individual-delete", args=[individual.id])

    selected_tags = list(individual.tags.all())
    tag_initial = [
        {"value": str(tag.id), "label": tag.name, "color": tag.color or "gray"}
        for tag in selected_tags
    ]
    organization_initial = []
    if individual.organization:
        organization_initial = [
            {
                "value": str(individual.organization_id),
                "label": individual.organization.name,
                "color": "gray",
            }
        ]
    city_initial = []
    if individual.location_city:
        city_initial = [
            {
                "value": str(individual.location_city_id),
                "label": f"{individual.location_city.name}{' (' + (individual.location_city.state.abbreviation or individual.location_city.state.name) + ')' if individual.location_city.state else ''}",
                "color": "gray",
            }
        ]
    state_initial = []
    if individual.location_state:
        state_initial = [
            {
                "value": str(individual.location_state_id),
                "label": individual.location_state.name,
                "color": "gray",
            }
        ]
    county_initial = []
    if individual.location_county:
        county_label_state = ""
        if individual.location_county.state:
            county_label_state = (
                individual.location_county.state.name
                or individual.location_county.state.abbreviation
                or ""
            )
        county_label = individual.location_county.name
        if county_label_state:
            county_label = f"{county_label} ({county_label_state})"
        county_initial = [
            {
                "value": str(individual.location_county_id),
                "label": county_label,
                "color": "gray",
            }
        ]
    zip_initial = []
    if individual.location_zip:
        zip_initial = [
            {
                "value": str(individual.location_zip_id),
                "label": individual.location_zip.zip_code_five_digit,
                "color": "gray",
            }
        ]

    context = {
        "individual": individual,
        "tags": tags,
        "organizations": organizations,
        "tag_initial": tag_initial,
        "organization_initial": organization_initial,
        "city_initial": city_initial,
        "state_initial": state_initial,
        "county_initial": county_initial,
        "zip_initial": zip_initial,
        "error": error,
        "success": success,
        "active_tab": active_tab,
        "is_new": is_new,
        "refresh_table": refresh_table,
        "list_refresh_url": _current_list_url(request, "crm-individuals"),
        "save_url": save_url,
        "delete_url": delete_url,
        "edit_url": edit_url,
    }
    return render(
        request, "cotton/app/gc_crm/partials/individual_drawer.html", context
    )


@login_required
def individual_delete_view(request, individual_id):
    """Delete an individual and return a simple acknowledgement."""
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    team = _get_active_team(request)
    individual = Individual.objects.filter(id=individual_id, team=team).first()
    if not individual:
        return HttpResponseBadRequest("Individual not found")

    individual.delete()
    return HttpResponse("Deleted")
