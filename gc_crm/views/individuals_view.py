from django.shortcuts import render


def get_crm_individuals(request):
    """Serve the individuals tab content or full shell."""
    if request.htmx:
        return render(request, "cotton/app/gc_crm/pages/individuals.html")

    context = {"workspace_template": "cotton/app/gc_crm/pages/index.html", "initial_tab": "individuals"}
    return render(request, "cotton/app/index.html", context)
