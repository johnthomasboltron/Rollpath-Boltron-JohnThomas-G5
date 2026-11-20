from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Level(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="levels"
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    grid_width = models.PositiveIntegerField(
        default=20,
        validators=[MinValueValidator(5), MaxValueValidator(50)]
    )

    grid_height = models.PositiveIntegerField(
        default=20,
        validators=[MinValueValidator(5), MaxValueValidator(50)]
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["creator", "title"],
                name="unique_level_title_per_creator"
            )
        ]

    def __str__(self):
        return self.title
