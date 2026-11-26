from django.contrib import admin
from .models import Level, ElementType, LevelElement


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "creator",
        "grid_width",
        "grid_height",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("title", "creator__username")


@admin.register(ElementType)
class ElementTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(LevelElement)
class LevelElementAdmin(admin.ModelAdmin):
    list_display = (
        "level",
        "element_type",
        "pos_x",
        "pos_y",
        "width",
        "height",
    )
    list_filter = ("element_type",)
    search_fields = ("level__title",)
