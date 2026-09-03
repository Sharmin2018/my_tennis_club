
from django import forms

from .models import Routine


class RoutineForm(forms.ModelForm):

    year = forms.ChoiceField(
        choices=[
            (year, str(year))
            for year in range(2025, 2050)
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    class Meta:

        model = Routine

        fields = [
            "subject_assignment",
            "day",
            "month",
            "year",
            "period",
            "room",
            "is_active",
        ]

        widgets = {

            "subject_assignment": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "day": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "month": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "period": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "room": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Room No"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

        labels = {

            "subject_assignment": "Subject / Teacher",
            "day": "Day",
            "month": "Month",
            "year": "Year",
            "period": "Period",
            "room": "Room No",
            "is_active": "Active",
        }
