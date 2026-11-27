from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


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


class ElementType(models.Model):

    class Type(models.TextChoices):
        WALL = "WALL", "Wall"
        HAZARD = "HAZARD", "Hazard"
        CHECKPOINT = "CHECKPOINT", "Checkpoint"
        ZONE = "ZONE", "Zone"

    name = models.CharField(
        max_length=20,
        choices=Type.choices,
        unique=True
    )

    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()


class LevelElement(models.Model):

    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name="elements"
    )

    element_type = models.ForeignKey(
        ElementType,
        on_delete=models.PROTECT,
        related_name="level_elements"
    )

    pos_x = models.PositiveIntegerField()
    pos_y = models.PositiveIntegerField()

    width = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    height = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["level", "element_type", "pos_x", "pos_y"],
                name="unique_element_type_position_per_level"
            )
        ]

    def clean(self):
        super().clean()

        if self.level_id:
            if self.pos_x + self.width > self.level.grid_width:
                raise ValidationError(
                    "Element exceeds the board's width."
                )

            if self.pos_y + self.height > self.level.grid_height:
                raise ValidationError(
                    "Element exceeds the board's height."
                )

    def __str__(self):
        return f"{self.element_type} - {self.level}"
