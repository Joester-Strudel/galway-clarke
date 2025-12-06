from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.db import IntegrityError
from django.shortcuts import redirect, render


def signup(request):
    """
    Register a new user account and log them in on success.
    """
    if request.user.is_authenticated:
        return redirect("marketing-home")

    context = {}
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if not email or not password1 or not password2:
            context["error"] = "Email and password are required."
        elif password1 != password2:
            context["error"] = "Passwords do not match."
        else:
            User = get_user_model()
            try:
                user = User.objects.create_user(
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name,
                )
            except IntegrityError:
                context["error"] = "An account with that email already exists."
            else:
                login(request, user)
                messages.success(request, "Welcome aboard!")
                return redirect("marketing-home")

    return render(request, "cotton/app/gc_users/pages/signup.html", context)
