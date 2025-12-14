# Django Imports
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from django.shortcuts import render

# First-Party Imports
from gc_crm.models import Status, Tag
from gc_crm.views.organizations_view import _get_active_team


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
        {"value": str(tag.id), "label": tag.name, "color": tag.color or "gray"} for tag in page_obj
    ]
    return render(
        request,
        "cotton/app/components/fields/remote_pill_select_options.html",
        {"options": options, "next_url": next_url},
    )
