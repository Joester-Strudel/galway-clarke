from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, render


def signout(request):
    """
    Log the user out after confirmation.
    """
    if request.method == "POST":
        logout(request)
        messages.info(request, "Signed out.")
        return redirect("marketing-home")

    return render(request, "cotton/app/gc_users/pages/signout.html")
