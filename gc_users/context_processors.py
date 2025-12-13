def organization_context(request):
    user_orgs = []
    active_org = None
    user_preferences = {}

    if getattr(request, "user", None) and request.user.is_authenticated:
        user_orgs = list(request.user.organizations.all())
        active_id = request.session.get("active_organization_id")
        active_org = next(
            (org for org in user_orgs if str(org.id) == str(active_id)), None
        )
        user_preferences = request.user.preferences or {}

    return {
        "user_organizations": user_orgs,
        "active_organization": active_org,
        "user_preferences": user_preferences,
    }
