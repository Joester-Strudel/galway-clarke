from django.shortcuts import redirect
from django.urls import reverse


class OrganizationRequirementMiddleware:
    """
    Ensure authenticated users have an active organization selected.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip checks for anonymous users.
        if request.user.is_authenticated:
            path = request.path
            exempt_paths = {
                reverse("signin"),
                reverse("signup"),
                reverse("signout"),
                reverse("select-organization"),
                reverse("create-team"),
                reverse("admin:index"),
            }
            if not path.startswith("/admin") and path not in exempt_paths and not path.startswith("/static/"):
                user_orgs = request.user.organizations.all()
                active_org_id = request.session.get("active_organization_id")

                if not user_orgs.exists():
                    return redirect("create-team")

                if not active_org_id or not user_orgs.filter(id=active_org_id).exists():
                    return redirect("select-organization")

        response = self.get_response(request)
        return response
