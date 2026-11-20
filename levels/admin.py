from django.contrib import admin
from .models import Level


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