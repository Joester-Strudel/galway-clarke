from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        return render(
            request,
            "cotton/app/index.html",
            {"workspace_template": "cotton/app/gc_dashboard/pages/index.html"},
        )

    return render(request, "cotton/app/gc_marketing/pages/index.html")
