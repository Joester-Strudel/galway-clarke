# Django Imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render

# First-Party Imports
from gc_crm.models import Tag
from gc_crm.views.organizations_view import _get_active_team
from gc_core.constants.colors import TAILWIND_COLOR_CHOICES


def _tags_context(team):
    tags = (
        Tag.objects.filter(team=team).order_by("name") if team else Tag.objects.none()
    )
    return {"team": team, "tags": tags, "tag_color_choices": TAILWIND_COLOR_CHOICES}


@login_required
def team_tags_drawer(request):
    """Render the tag drawer partial."""
    team = _get_active_team(request)
    context = _tags_context(team)
    return render(request, "cotton/app/gc_users/partials/tag_drawer.html", context)


@login_required
def create_tag(request):
    """Create a new tag for the active team."""
    team = _get_active_team(request)
    if not team:
        return HttpResponseBadRequest("No active team")

    name = request.POST.get("name", "").strip()
    color = request.POST.get("color") or "gray"
    if not name:
        context = _tags_context(team) | {"error": "Name is required."}
        return render(
            request, "cotton/app/gc_users/partials/tag_drawer.html", context, status=400
        )

    Tag.objects.create(team=team, name=name, color=color)
    context = _tags_context(team)
    return render(request, "cotton/app/gc_users/partials/tag_drawer.html", context)


@login_required
def update_tag(request, tag_id):
    """Update an existing tag for the active team."""
    team = _get_active_team(request)
    tag = Tag.objects.filter(id=tag_id, team=team).first()
    if not tag:
        return HttpResponseBadRequest("Tag not found")

    tag.name = request.POST.get("name", "").strip() or tag.name
    tag.color = request.POST.get("color") or tag.color or "gray"
    tag.save()

    context = _tags_context(team)
    return render(request, "cotton/app/gc_users/partials/tag_drawer.html", context)


@login_required
def delete_tag(request, tag_id):
    """Delete a tag for the active team."""
    team = _get_active_team(request)
    tag = Tag.objects.filter(id=tag_id, team=team).first()
    if tag:
        tag.delete()

    context = _tags_context(team)
    return render(request, "cotton/app/gc_users/partials/tag_drawer.html", context)
