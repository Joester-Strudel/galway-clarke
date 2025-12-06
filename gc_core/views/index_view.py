from django.shortcuts import render


def index(request):
    template = (
        "cotton/app/index.html"
        if request.user.is_authenticated
        else "cotton/app/gc_marketing/pages/index.html"
    )
    return render(request, template)
