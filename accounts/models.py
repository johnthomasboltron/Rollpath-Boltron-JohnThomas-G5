from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Role(models.TextChoices):
        CREATOR = "CREATOR", "Creator"
        TESTER = "TESTER", "Tester"
        ADMIN = "ADMIN", "Admin"

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.TESTER
    )

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    display_name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.display_name