# Django Imports
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse

from gc_core.constants.colors import TAILWIND_COLOR_CHOICES
from django.contrib.auth import get_user_model
from gc_crm.views.organizations_view import _get_active_team


@login_required
def team_settings(request, tab="members"):
    """
    Render the Team Settings workspace. Serve the fragment for HTMX requests and
    the full shell otherwise so direct navigation works.
    """
    initial_tab = tab if tab in ("members", "field-definitions") else "members"
    if (
        initial_tab == "members"
        and request.path == reverse("settings")
        and request.headers.get("HX-Request") != "true"
    ):
        return redirect("settings-members")
    template = "cotton/app/gc_users/pages/team_settings.html"
    team = _get_active_team(request)
    search_query = request.GET.get("search", "").strip()
    sort_field = request.GET.get("sort", "name")
    sort_direction = request.GET.get("direction", "asc")

    allowed_sorts = {
        "name": ("first_name", "last_name", "email"),
        "email": ("email", "first_name", "last_name"),
    }
    sort_field = sort_field if sort_field in allowed_sorts else "name"
    sort_direction = "desc" if sort_direction == "desc" else "asc"
    sort_expr = allowed_sorts[sort_field]
    if sort_direction == "desc":
        sort_expr = [f"-{field}" for field in sort_expr]

    qs = team.users.all() if team else get_user_model().objects.none()
    if search_query:
        qs = qs.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
        )
    qs = qs.order_by(*sort_expr)

    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "team": team,
        "members": page_obj,
        "page_obj": page_obj,
        "search_query": search_query,
        "sort_field": sort_field,
        "sort_direction": sort_direction,
        "filter_querystring": "",
        "filter_fields": [],
        "status_color_choices": TAILWIND_COLOR_CHOICES,
        "initial_tab": initial_tab,
    }

    if request.headers.get("HX-Request") == "true":
        return render(request, template, context)

    return render(
        request,
        "cotton/app/index.html",
        {"workspace_template": template, **context},
    )
