from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Registration
    path("register/", views.register, name="register"),

    # Login
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html"
        ),
        name="login"
    ),

    # Logout
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    # General dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Role-based dashboards
    path("dashboard/creator/", views.creator_dashboard, name="creator_dashboard"),
    path("dashboard/tester/", views.tester_dashboard, name="tester_dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("profile/", views.profile, name="profile"),
]