from django import forms
from .models import Level, LevelElement


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


class LevelElementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.level = kwargs.pop("level", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = LevelElement
        fields = [
            "element_type",
            "pos_x",
            "pos_y",
            "width",
            "height",
        ]

        widgets = {
            "pos_x": forms.NumberInput(attrs={"min": 0}),
            "pos_y": forms.NumberInput(attrs={"min": 0}),
            "width": forms.NumberInput(attrs={"min": 1}),
            "height": forms.NumberInput(attrs={"min": 1}),
        }

    def clean(self):
        cleaned_data = super().clean()

        element_type = cleaned_data.get("element_type")
        pos_x = cleaned_data.get("pos_x")
        pos_y = cleaned_data.get("pos_y")
        width = cleaned_data.get("width")
        height = cleaned_data.get("height")

        if not self.level:
            raise forms.ValidationError(
                "A level must be selected."
            )

        if None in (pos_x, pos_y, width, height):
            return cleaned_data

        if pos_x + width > self.level.grid_width:
            self.add_error(
                "width",
                "Element exceeds the board's width."
            )

        if pos_y + height > self.level.grid_height:
            self.add_error(
                "height",
                "Element exceeds the board's height."
            )

        if element_type:
            duplicate = LevelElement.objects.filter(
                level=self.level,
                element_type=element_type,
                pos_x=pos_x,
                pos_y=pos_y,
            ).exclude(pk=self.instance.pk).exists()

            if duplicate:
                self.add_error(
                    "element_type",
                    "This element type already occupies that position."
                )

        return cleaned_data
