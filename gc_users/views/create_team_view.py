from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from gc_users.models import Team


@login_required
def create_team(request):
    """
    Allow a user to create a new team and attach themselves to it.
    """
    # Clear any previous messages so this screen shows only its own context.
    list(messages.get_messages(request))

    if request.method == "GET":
        messages.info(request, "Create a team to continue.")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if not name:
            messages.error(request, "Team name is required.")
        else:
            team = Team.objects.create(name=name, owner=request.user)
            team.users.add(request.user)
            request.session["active_organization_id"] = str(team.id)
            messages.success(request, "Team created.")
            return redirect("marketing-home")

    return render(request, "cotton/app/gc_users/pages/create_team.html")
