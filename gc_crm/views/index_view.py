from django.shortcuts import render


def get_crm_index(request):
    """
    Render the CRM contacts page. If this is an HTMX request, return only the
    contacts fragment; otherwise return the full shell.
    """
    context = {
        "workspace_template": "cotton/app/gc_crm/pages/index.html",
        "initial_tab": "organizations",
    }

    htmx_context = {"initial_tab": "organizations"}

    if request.htmx:
        return render(request, "cotton/app/gc_crm/pages/index.html", htmx_context)

    return render(request, "cotton/app/index.html", context)
