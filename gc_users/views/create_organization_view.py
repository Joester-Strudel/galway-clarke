from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from gc_users.models import Organization


@login_required
def create_organization(request):
    """
    Allow a user to create a new organization and attach themselves to it.
    """
    # Clear any previous messages so this screen shows only its own context.
    list(messages.get_messages(request))

    if request.method == "GET":
        messages.info(request, "Create an organization to continue.")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if not name:
            messages.error(request, "Organization name is required.")
        else:
            org = Organization.objects.create(name=name, owner=request.user)
            org.users.add(request.user)
            request.session["active_organization_id"] = str(org.id)
            messages.success(request, "Organization created.")
            return redirect("marketing-home")

    return render(request, "cotton/app/gc_users/pages/create_organization.html")
