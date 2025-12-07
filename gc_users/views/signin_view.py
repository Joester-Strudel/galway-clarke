from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


def signin(request):
    """
    Authenticate an existing user and start their session.
    """
    if request.user.is_authenticated:
        return redirect("marketing-home")

    context = {}
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

            # If the user belongs to multiple organizations, let them pick one.
            org_qs = user.organizations.all()
            if not org_qs.exists():
                messages.info(request, "Create an organization to continue.")
                return redirect("create-organization")
            if org_qs.count() == 1:
                request.session["active_organization_id"] = org_qs.first().id
                messages.success(request, "Signed in successfully.")
                return redirect("marketing-home")
            if org_qs.count() > 1:
                messages.info(request, "Choose an organization to continue.")
                return redirect("select-organization")

            messages.success(request, "Signed in successfully.")
            return redirect("marketing-home")

        context["error"] = "Invalid email or password."

    return render(request, "cotton/app/gc_users/pages/signin.html", context)
