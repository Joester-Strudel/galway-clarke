# Django Imports
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpResponseBadRequest
from django.shortcuts import render

# First-Party Imports
from gc_crm.models import Status, Tag, Industry, Individual
from gc_crm.views.organizations_view import _get_active_team
from gc_geography.models import City, State, County, ZipCode


def _paginate_options(queryset, request):
    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(name__icontains=search)
    paginator = Paginator(queryset.order_by("name"), 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    next_url = None
    if page_obj.has_next():
        params = request.GET.copy()
        params["page"] = page_obj.next_page_number()
        querystring = params.urlencode()
        next_url = f"{request.path}?{querystring}"
    return page_obj, next_url


@login_required
def select_statuses(request):
    team = _get_active_team(request)
    if not team:
        return HttpResponseBadRequest("No active team")
    qs = Status.objects.filter(team=team)
    page_obj, next_url = _paginate_options(qs, request)
    options = [
        {"value": str(status.id), "label": status.name, "color": status.color or "gray"}
        for status in page_obj
    ]
    return render(
        request,
        "cotton/app/components/fields/remote_pill_select_options.html",
        {"options": options, "next_url": next_url},
    )


@login_required
def select_tags(request):
    team = _get_active_team(request)
    if not team:
        return HttpResponseBadRequest("No active team")
    qs = Tag.objects.filter(team=team)
    page_obj, next_url = _paginate_options(qs, request)
    options = [
        {"value": str(tag.id), "label": tag.name, "color": tag.color or "gray"}
        for tag in page_obj
    ]
    return render(
        request,
        "cotton/app/components/fields/remote_pill_select_options.html",
        {"options": options, "next_url": next_url},
    )


@login_required
def select_industries(request):
    team = _get_active_team(request)
    if not team:
        return HttpResponseBadRequest("No active team")
    qs = Industry.objects.filter(team=team)
    page_obj, next_url = _paginate_options(qs, request)
    options = [
        {
            "value": str(industry.id),
            "label": industry.name,
            "color": industry.color or "gray",
        }
        for industry in page_obj
    ]
    return render(
        request,
        "cotton/app/components/fields/remote_pill_select_options.html",
        {"options": options, "next_url": next_url},
    )


@login_required
def select_individuals(request):
    team = _get_active_team(request)
    if not team:
        return HttpResponseBadRequest("No active team")
    qs = Individual.objects.filter(team=team)
    search = request.GET.get("search", "").strip()
    if search:
        qs = qs.filter(
            models.Q(first_name__icontains=search)
            | models.Q(last_name__icontains=search)
            | models.Q(email__icontains=search)
        )
    paginator = Paginator(qs.order_by("last_name", "first_name"), 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    next_url = None
    if page_obj.has_next():
        params = request.GET.copy()
        params["page"] = page_obj.next_page_number()
        querystring = params.urlencode()
        next_url = f"{request.path}?{querystring}"
    options = [
        {
            "value": str(person.id),
            "label": (
                f"{person.first_name} {person.last_name}".strip()
                or person.email
                or "Unnamed"
            ).strip(),
            "color": "gray",
        }
        for person in page_obj
    ]
    return render(
        request,
        "cotton/app/components/fields/remote_pill_select_options.html",
        {"options": options, "next_url": next_url},
    )


@login_required
def select_cities(request):
    qs = City.objects.select_related("state")
    page_obj, next_url = _paginate_options(qs, request)
    options = [
        {
            "value": str(city.id),
            "label": f"{city.name}{' (' + (city.state.abbreviation or city.state.name) + ')' if city.state else ''}",
            "color": "gray",
        }
        for city in page_obj
    ]
    return render(
        request,
        "cotton/app/components/fields/remote_pill_select_options.html",
        {"options": options, "next_url": next_url},
    )


@login_required
def select_states(request):
    qs = State.objects.all()
    page_obj, next_url = _paginate_options(qs, request)
    options = [
        {"value": str(state.id), "label": state.name, "color": "gray"}
        for state in page_obj
    ]
    return render(
        request,
        "cotton/app/components/fields/remote_pill_select_options.html",
        {"options": options, "next_url": next_url},
    )


@login_required
def select_counties(request):
    qs = County.objects.all()
    page_obj, next_url = _paginate_options(qs, request)
    options = [
        {
            "value": str(county.id),
            "label": f"{county.name}{' (' + (county.state.abbreviation or county.state.name) + ')' if county.state else ''}",
            "color": "gray",
        }
        for county in page_obj
    ]
    return render(
        request,
        "cotton/app/components/fields/remote_pill_select_options.html",
        {"options": options, "next_url": next_url},
    )


@login_required
def select_zip_codes(request):
    qs = ZipCode.objects.all()
    search = request.GET.get("search", "").strip()
    if search:
        qs = qs.filter(zip_code_five_digit__icontains=search)
    paginator = Paginator(qs.order_by("zip_code_five_digit"), 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    next_url = None
    if page_obj.has_next():
        params = request.GET.copy()
        params["page"] = page_obj.next_page_number()
        querystring = params.urlencode()
        next_url = f"{request.path}?{querystring}"
    options = [
        {
            "value": str(zip_code.id),
            "label": zip_code.zip_code_five_digit,
            "color": "gray",
        }
        for zip_code in page_obj
    ]
    return render(
        request,
        "cotton/app/components/fields/remote_pill_select_options.html",
        {"options": options, "next_url": next_url},
    )
