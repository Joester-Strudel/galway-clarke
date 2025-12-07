from django.shortcuts import render


def get_crm_index(request):
    """
    Render the CRM contacts page. If this is an HTMX request, return only the
    contacts fragment; otherwise return the full shell.
    """
    if request.headers.get("HX-Request") == "true":
        return render(request, "cotton/app/gc_crm/pages/index.html")

    return render(request, "cotton/app/index.html", {"workspace_template": "cotton/app/gc_crm/pages/index.html"})
