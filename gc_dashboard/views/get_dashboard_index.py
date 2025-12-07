from django.shortcuts import redirect, render


def get_dashboard_index(request):
    """
    Render the dashboard page. If this is an HTMX request, return only the
    dashboard fragment; otherwise return the full shell.
    """
    if request.headers.get("HX-Request") == "true":
        return render(request, "cotton/app/gc_dashboard/pages/index.html")

    # For non-HTMX requests, render the full shell with the dashboard content preloaded.
    return render(request, "cotton/app/index.html", {"workspace_template": "cotton/app/gc_dashboard/pages/index.html"})
