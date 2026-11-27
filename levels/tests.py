from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Level

User = get_user_model()


class LevelManagementTests(TestCase):

    def setUp(self):
        self.creator = User.objects.create_user(
            username="creator1",
            email="creator1@test.com",
            password="TestPass123!",
            role="CREATOR"
        )

        self.other_creator = User.objects.create_user(
            username="creator2",
            email="creator2@test.com",
            password="TestPass123!",
            role="CREATOR"
        )

        self.tester = User.objects.create_user(
            username="tester1",
            email="tester1@test.com",
            password="TestPass123!",
            role="TESTER"
        )

        self.level = Level.objects.create(
            creator=self.creator,
            title="Test Level",
            description="A test puzzle",
            grid_width=20,
            grid_height=20
        )

    def test_valid_level_creation(self):
        self.client.login(username="creator1", password="TestPass123!")

        response = self.client.post(reverse("level_create"), {
            "title": "New Level",
            "description": "A new puzzle",
            "grid_width": 20,
            "grid_height": 20
        })

        self.assertEqual(Level.objects.filter(title="New Level").count(), 1)

    def test_invalid_level_dimensions(self):
        self.client.login(username="creator1", password="TestPass123!")

        response = self.client.post(reverse("level_create"), {
            "title": "Invalid Level",
            "description": "Invalid dimensions",
            "grid_width": 2,
            "grid_height": 20
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Level.objects.filter(title="Invalid Level").exists())

    def test_login_required_for_level_list(self):
        response = self.client.get(reverse("level_list"))

        self.assertEqual(response.status_code, 302)

    def test_tester_cannot_create_level(self):
        self.client.login(username="tester1", password="TestPass123!")

        response = self.client.get(reverse("level_create"))

        self.assertEqual(response.status_code, 403)

    def test_user_cannot_view_another_users_level(self):
        self.client.login(username="creator2", password="TestPass123!")

        response = self.client.get(
            reverse("level_detail", args=[self.level.pk])
        )

        self.assertEqual(response.status_code, 403)

    def test_user_cannot_edit_another_users_level(self):
        self.client.login(username="creator2", password="TestPass123!")

        response = self.client.get(
            reverse("level_update", args=[self.level.pk])
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_requires_post(self):
        self.client.login(username="creator1", password="TestPass123!")

        response = self.client.get(
            reverse("level_delete", args=[self.level.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Level.objects.filter(pk=self.level.pk).exists())

    def test_successful_level_deletion(self):
        self.client.login(username="creator1", password="TestPass123!")

        response = self.client.post(
            reverse("level_delete", args=[self.level.pk])
        )

        self.assertFalse(Level.objects.filter(pk=self.level.pk).exists())

    def test_invalid_level_id_returns_404(self):
        self.client.login(username="creator1", password="TestPass123!")

        response = self.client.get(
            reverse("level_detail", args=[999999])
        )

        self.assertEqual(response.status_code, 404)
