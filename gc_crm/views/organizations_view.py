from django.shortcuts import render


def organizations_view(request):
    """Serve the organizations tab content or full shell."""
    if request.htmx:
        return render(request, "cotton/app/gc_crm/pages/organizations.html")

    context = {"workspace_template": "cotton/app/gc_crm/pages/index.html", "initial_tab": "organizations",}
    return render(request, "cotton/app/index.html", context)
