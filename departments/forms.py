from django import forms
from .models import Department


class DepartmentForm(forms.ModelForm):

    class Meta:

        model = Department

        fields = "__all__"

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Department Name"
                }
            ),

            "department_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Department Code"
                }
            ),

        }