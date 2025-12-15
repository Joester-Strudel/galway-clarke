# Django Imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render

# First-Party Imports
from gc_crm.models import Industry
from gc_crm.views.organizations_view import _get_active_team
from gc_core.constants.colors import TAILWIND_COLOR_CHOICES


def _industries_context(team):
    industries = Industry.objects.filter(team=team).order_by("name") if team else Industry.objects.none()
    return {"team": team, "industries": industries, "industry_color_choices": TAILWIND_COLOR_CHOICES}


@login_required
def team_industries_drawer(request):
    """Render the industry drawer partial."""
    team = _get_active_team(request)
    context = _industries_context(team)
    return render(request, "cotton/app/gc_users/partials/industry_drawer.html", context)


@login_required
def create_industry(request):
    """Create a new industry for the active team."""
    team = _get_active_team(request)
    if not team:
        return HttpResponseBadRequest("No active team")

    name = request.POST.get("name", "").strip()
    color = request.POST.get("color") or "gray"
    if not name:
        context = _industries_context(team) | {"error": "Name is required."}
        return render(
            request,
            "cotton/app/gc_users/partials/industry_drawer.html",
            context,
            status=400,
        )

    Industry.objects.create(team=team, name=name, color=color)
    context = _industries_context(team)
    return render(request, "cotton/app/gc_users/partials/industry_drawer.html", context)


@login_required
def update_industry(request, industry_id):
    """Update an existing industry for the active team."""
    team = _get_active_team(request)
    industry = Industry.objects.filter(id=industry_id, team=team).first()
    if not industry:
        return HttpResponseBadRequest("Industry not found")

    industry.name = request.POST.get("name", "").strip() or industry.name
    industry.color = request.POST.get("color") or industry.color or "gray"
    industry.save()

    context = _industries_context(team)
    return render(request, "cotton/app/gc_users/partials/industry_drawer.html", context)


@login_required
def delete_industry(request, industry_id):
    """Delete an industry for the active team."""
    team = _get_active_team(request)
    industry = Industry.objects.filter(id=industry_id, team=team).first()
    if industry:
        industry.delete()

    context = _industries_context(team)
    return render(request, "cotton/app/gc_users/partials/industry_drawer.html", context)
