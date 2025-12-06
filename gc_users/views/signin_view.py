from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


def signin(request):
    """
    Authenticate an existing user and start their session.
    """
    if request.user.is_authenticated:
        return redirect("marketing-home")

    context = {}
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Signed in successfully.")
            return redirect("marketing-home")

        context["error"] = "Invalid email or password."

    return render(request, "cotton/app/gc_users/pages/signin.html", context)
