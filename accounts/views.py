from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import RegistrationForm, ProfileForm
from .models import Profile


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            Profile.objects.create(
                user=user,
                display_name=user.username
            )

            messages.success(
                request,
                "Your account has been created successfully!"
            )

            return redirect("login")

    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


@login_required
def dashboard(request):
    if request.user.role == "CREATOR":
        return redirect("creator_dashboard")

    elif request.user.role == "TESTER":
        return redirect("tester_dashboard")

    elif request.user.role == "ADMIN":
        return redirect("admin_dashboard")

    return HttpResponseForbidden("Invalid account role.")


@login_required
def creator_dashboard(request):
    if request.user.role != "CREATOR":
        return HttpResponseForbidden("Access denied.")

    return render(request, "accounts/creator_dashboard.html")


@login_required
def tester_dashboard(request):
    if request.user.role != "TESTER":
        return HttpResponseForbidden("Access denied.")

    return render(request, "accounts/tester_dashboard.html")


@login_required
def admin_dashboard(request):
    if request.user.role != "ADMIN":
        return HttpResponseForbidden("Access denied.")

    return render(request, "accounts/admin_dashboard.html")


@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"display_name": request.user.username}
    )

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            instance=user_profile
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Profile updated successfully!"
            )
            return redirect("profile")

    else:
        form = ProfileForm(instance=user_profile)

    return render(
        request,
        "accounts/profile.html",
        {"form": form, "profile": user_profile}
    )