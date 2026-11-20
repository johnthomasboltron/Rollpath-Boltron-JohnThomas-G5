from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    role = forms.ChoiceField(
        choices=[
            (User.Role.CREATOR, "Creator"),
            (User.Role.TESTER, "Tester"),
        ],
        initial=User.Role.TESTER
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "role",
            "password1",
            "password2",
        ]


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["display_name", "bio"]