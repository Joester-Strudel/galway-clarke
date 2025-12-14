# Django Imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render

# First-Party Imports
from gc_crm.models import Status
from gc_crm.views.organizations_view import _get_active_team
from gc_core.constants.colors import TAILWIND_COLOR_CHOICES


def _statuses_context(team):
    statuses = (
        Status.objects.filter(team=team).order_by("name") if team else Status.objects.none()
    )
    return {"team": team, "statuses": statuses, "status_color_choices": TAILWIND_COLOR_CHOICES}


@login_required
def team_status_drawer(request):
    """Render the status drawer partial."""
    team = _get_active_team(request)
    context = _statuses_context(team)
    return render(request, "cotton/app/gc_users/partials/status_drawer.html", context)


@login_required
def create_status(request):
    """Create a new status for the active team."""
    team = _get_active_team(request)
    if not team:
        return HttpResponseBadRequest("No active team")

    name = request.POST.get("name", "").strip()
    color = request.POST.get("color") or "gray"
    if not name:
        context = _statuses_context(team) | {"error": "Name is required."}
        return render(request, "cotton/app/gc_users/partials/status_drawer.html", context, status=400)

    Status.objects.create(team=team, name=name, color=color)
    context = _statuses_context(team)
    return render(request, "cotton/app/gc_users/partials/status_drawer.html", context)


@login_required
def update_status(request, status_id):
    """Update an existing status for the active team."""
    team = _get_active_team(request)
    status = Status.objects.filter(id=status_id, team=team).first()
    if not status:
        return HttpResponseBadRequest("Status not found")

    status.name = request.POST.get("name", "").strip() or status.name
    status.color = request.POST.get("color") or status.color
    status.save()

    context = _statuses_context(team)
    return render(request, "cotton/app/gc_users/partials/status_drawer.html", context)


@login_required
def delete_status(request, status_id):
    """Delete a status for the active team."""
    team = _get_active_team(request)
    status = Status.objects.filter(id=status_id, team=team).first()
    if status:
        status.delete()

    context = _statuses_context(team)
    return render(request, "cotton/app/gc_users/partials/status_drawer.html", context)
