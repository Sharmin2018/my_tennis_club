from django import forms
from .models import Teacher


class TeacherForm(forms.ModelForm):

    class Meta:

        model = Teacher

        exclude = ["created_by"]

        widgets = {

            "name": forms.TextInput(attrs={
                "class": "form-control"
             }),

            "designation": forms.Select(attrs={
                 "class": "form-select"
            }),

            "department": forms.Select(attrs={
                "class": "form-select"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "joining_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "dob": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "religion": forms.Select(attrs={
                "class": "form-select"
            }),

            "gender": forms.Select(attrs={
                "class": "form-select"
            }),

            "photo": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
    }