from django.shortcuts import render

from gc_dashboard.views.get_dashboard_index import _dashboard_stats


def index(request):
    if request.user.is_authenticated:
        stats = _dashboard_stats(request)
        return render(
            request,
            "cotton/app/index.html",
            {"workspace_template": "cotton/app/gc_dashboard/pages/index.html", **stats},
        )

    return render(request, "cotton/app/gc_marketing/pages/index.html")
