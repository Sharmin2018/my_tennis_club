from django import forms

from .models import Routine


class RoutineForm(forms.ModelForm):

    class Meta:
        model = Routine

        fields = [
            "subject_assignment",
            "day",
            "period",
            "room",
            "is_active",
        ]

        widgets = {
            "subject_assignment": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_subject_assignment",
                }
            ),

            "day": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_day",
                }
            ),

            "period": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_period",
                }
            ),

            "room": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "id_room",
                    "placeholder": "Room No",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }