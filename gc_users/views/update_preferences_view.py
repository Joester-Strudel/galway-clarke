import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def update_preferences(request):
    """
    Persist user preferences (e.g., nav collapse) into the user.preferences JSON field.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        payload = {}

    user = request.user
    prefs = user.preferences or {}
    prefs.update(payload)
    user.preferences = prefs
    user.save(update_fields=["preferences"])
    return JsonResponse({"status": "ok", "preferences": user.preferences})
