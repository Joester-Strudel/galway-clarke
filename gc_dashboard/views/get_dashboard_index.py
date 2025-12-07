from django.shortcuts import render


def get_dashboard_index(request):
    """
    Render the dashboard page. If this is an HTMX request, return only the
    dashboard fragment; otherwise return the full shell.
    """
    if request.headers.get("HX-Request") == "true":
        return render(request, "cotton/app/gc_dashboard/pages/index.html")

    return render(request, "cotton/app/index.html")
