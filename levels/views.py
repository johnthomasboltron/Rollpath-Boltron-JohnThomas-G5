from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Level, LevelElement
from .forms import (
    LevelForm,
    LevelElementForm,
    LevelElementMoveForm,
    LevelElementResizeForm,
)


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

        if not level.elements.exists():
            messages.error(
                request,
                "You must add at least one element before publishing."
            )
            return redirect("level_detail", pk=level.pk)

        level.status = Level.Status.PUBLISHED
        level.published_at = timezone.now()
        level.save(update_fields=["status", "published_at"])

        messages.success(request, "Level published successfully!")

    return redirect("level_detail", pk=level.pk)


@login_required
def level_editor(request, pk):
    level = get_object_or_404(Level, pk=pk)

    if level.creator != request.user and not request.user.is_superuser:
        raise PermissionDenied

    if not creator_required(request.user):
        raise PermissionDenied

    if request.method == "POST":
        form = LevelElementForm(request.POST, level=level)

        if form.is_valid():
            element = form.save(commit=False)
            element.level = level
            element.save()

            messages.success(request, "Element added successfully!")
            return redirect("level_editor", pk=level.pk)

    else:
        form = LevelElementForm(level=level)

    elements = list(
        level.elements.select_related(
            "element_type"
        ).order_by("pos_y", "pos_x")
    )

    board_rows = []

    for y in range(level.grid_height):
        row = []

        for x in range(level.grid_width):
            placed_element = next(
                (
                    element for element in elements
                    if element.pos_x <= x < element.pos_x + element.width
                    and element.pos_y <= y < element.pos_y + element.height
                ),
                None
            )

            row.append(placed_element)

        board_rows.append(row)

    return render(request, "levels/level_editor.html", {
        "level": level,
        "form": form,
        "elements": elements,
        "board_rows": board_rows,
    })

@login_required
def level_element_delete(request, pk, element_pk):
    if request.method != "POST":
        raise PermissionDenied

    level = get_object_or_404(Level, pk=pk)

    if level.creator != request.user and not request.user.is_superuser:
        raise PermissionDenied

    if not creator_required(request.user):
        raise PermissionDenied

    element = get_object_or_404(
        LevelElement,
        pk=element_pk,
        level=level
    )

    element.delete()

    messages.success(request, "Element removed successfully!")
    return redirect("level_editor", pk=level.pk)

@login_required
def level_element_move(request, pk, element_pk):
    if request.method != "POST":
        raise PermissionDenied

    level = get_object_or_404(Level, pk=pk)

    if level.creator != request.user and not request.user.is_superuser:
        raise PermissionDenied

    if not creator_required(request.user):
        raise PermissionDenied

    element = get_object_or_404(
        LevelElement,
        pk=element_pk,
        level=level
    )

    form = LevelElementMoveForm(
        request.POST,
        instance=element,
        level=level
    )

    if form.is_valid():
        form.save()
        messages.success(request, "Element moved successfully!")
    else:
        messages.error(request, "Could not move element. Check its coordinates.")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

    return redirect("level_editor", pk=level.pk)

@login_required
def level_element_resize(request, pk, element_pk):
    if request.method != "POST":
        raise PermissionDenied

    level = get_object_or_404(Level, pk=pk)

    if level.creator != request.user and not request.user.is_superuser:
        raise PermissionDenied

    if not creator_required(request.user):
        raise PermissionDenied

    element = get_object_or_404(
        LevelElement,
        pk=element_pk,
        level=level
    )

    form = LevelElementResizeForm(
        request.POST,
        instance=element,
        level=level
    )

    if form.is_valid():
        form.save()
        messages.success(request, "Element resized successfully!")
    else:
        messages.error(request, "Could not resize element.")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

    return redirect("level_editor", pk=level.pk)