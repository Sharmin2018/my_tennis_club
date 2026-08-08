from django import forms
from .models import Routine


class RoutineForm(forms.ModelForm):

    class Meta:
        model = Routine
        fields = "__all__"

        widgets = {
            "subject_assignment": forms.Select(attrs={"class": "form-select"}),
            "day": forms.Select(attrs={"class": "form-select"}),
            "start_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time"
            }),
            "end_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time"
            }),
            "room": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Room Number"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }