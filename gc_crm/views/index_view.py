from django.shortcuts import render


def index_view(request):
    """
    Render the CRM contacts page. If this is an HTMX request, return only the
    contacts fragment; otherwise return the full shell.
    """
    if request.htmx:
        return render(request, "cotton/app/gc_crm/pages/index.html", {"initial_tab": "organizations"})

    context = {"workspace_template": "cotton/app/gc_crm/pages/index.html", "initial_tab": "organizations"}
    return render(request, "cotton/app/index.html", context)
