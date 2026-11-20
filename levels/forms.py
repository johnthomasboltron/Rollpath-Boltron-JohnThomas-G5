from django import forms
from .models import Level


class LevelForm(forms.ModelForm):

    class Meta:
        model = Level
        fields = [
            "title",
            "description",
            "grid_width",
            "grid_height",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Enter level title"
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Describe your level"
            }),
            "grid_width": forms.NumberInput(attrs={
                "min": 5,
                "max": 50
            }),
            "grid_height": forms.NumberInput(attrs={
                "min": 5,
                "max": 50
            }),
        }

    def clean_grid_width(self):
        width = self.cleaned_data["grid_width"]

        if not 5 <= width <= 50:
            raise forms.ValidationError(
                "Board width must be between 5 and 50."
            )

        return width

    def clean_grid_height(self):
        height = self.cleaned_data["grid_height"]

        if not 5 <= height <= 50:
            raise forms.ValidationError(
                "Board height must be between 5 and 50."
            )

        return height