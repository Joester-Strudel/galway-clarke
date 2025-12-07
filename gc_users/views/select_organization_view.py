from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def select_organization(request):
    """
    Let a signed-in user choose which organization to act under.
    """
    # Clear any previous messages so this screen shows only its own context.
    list(messages.get_messages(request))

    orgs = request.user.organizations.all()

    if not orgs.exists():
        messages.info(request, "Create an organization to continue.")
        return redirect("create-organization")

    org_id = request.POST.get("organization_id") if request.method == "POST" else request.GET.get("organization_id")
    if org_id and orgs.filter(id=org_id).exists():
        request.session["active_organization_id"] = str(org_id)
        messages.success(request, "Organization selected.")
        return redirect("marketing-home")

    return render(
        request,
        "cotton/app/gc_users/pages/select_organization.html",
        {"organizations": orgs},
    )
