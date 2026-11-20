from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Level
from .forms import LevelForm


def creator_required(user):
    return user.role == "CREATOR" or user.is_superuser


@login_required
def level_list(request):
    levels = Level.objects.filter(creator=request.user).order_by("-created_at")

    return render(request, "levels/level_list.html", {
        "levels": levels
    })


@login_required
def level_create(request):
    if not creator_required(request.user):
        raise PermissionDenied

    if request.method == "POST":
        form = LevelForm(request.POST)

        if form.is_valid():
            level = form.save(commit=False)
            level.creator = request.user
            level.save()

            messages.success(request, "Level created successfully!")
            return redirect("level_detail", pk=level.pk)

    else:
        form = LevelForm()

    return render(request, "levels/level_form.html", {
        "form": form,
        "page_title": "Create Level"
    })


@login_required
def level_detail(request, pk):
    level = get_object_or_404(Level, pk=pk)

    if level.creator != request.user and not request.user.is_superuser:
        raise PermissionDenied

    return render(request, "levels/level_detail.html", {
        "level": level
    })


@login_required
def level_update(request, pk):
    level = get_object_or_404(Level, pk=pk)

    if level.creator != request.user and not request.user.is_superuser:
        raise PermissionDenied

    if not creator_required(request.user):
        raise PermissionDenied

    if request.method == "POST":
        form = LevelForm(request.POST, instance=level)

        if form.is_valid():
            form.save()
            messages.success(request, "Level updated successfully!")
            return redirect("level_detail", pk=level.pk)

    else:
        form = LevelForm(instance=level)

    return render(request, "levels/level_form.html", {
        "form": form,
        "page_title": "Edit Level"
    })


@login_required
def level_delete(request, pk):
    level = get_object_or_404(Level, pk=pk)

    if level.creator != request.user and not request.user.is_superuser:
        raise PermissionDenied

    if not creator_required(request.user):
        raise PermissionDenied

    if request.method == "POST":
        level.delete()
        messages.success(request, "Level deleted successfully!")
        return redirect("level_list")

    return render(request, "levels/level_confirm_delete.html", {
        "level": level
    })


@login_required
def level_publish(request, pk):
    level = get_object_or_404(Level, pk=pk)

    if level.creator != request.user and not request.user.is_superuser:
        raise PermissionDenied

    if not creator_required(request.user):
        raise PermissionDenied

    if request.method == "POST":
        level.status = Level.Status.PUBLISHED
        level.published_at = timezone.now()
        level.save(update_fields=["status", "published_at"])

        messages.success(request, "Level published successfully!")

    return redirect("level_detail", pk=level.pk)