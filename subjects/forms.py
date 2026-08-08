from django import forms
from .models import Subject
from .models import SubjectAssignment


class SubjectForm(forms.ModelForm):

    class Meta:

        model = Subject

        fields = "__all__"

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class":"form-control"
                }
            ),

            "code": forms.TextInput(
                attrs={
                    "class":"form-control"
                }
            ),

            "department": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "student_class": forms.Select(
                attrs={
                    "class":"form-select"
                }
            ),

            "full_marks": forms.NumberInput(
                attrs={
                    "class":"form-control"
                }
            ),

            "pass_marks": forms.NumberInput(
                attrs={
                    "class":"form-control"
                }
            ),

            "credit": forms.NumberInput(
                attrs={
                    "class":"form-control"
                }
            ),

            "is_optional": forms.CheckboxInput(
                attrs={
                    "class":"form-check-input"
                }
            ),

        }


class SubjectAssignmentForm(forms.ModelForm):

    class Meta:
        model = SubjectAssignment
        fields = "__all__"

        widgets = {
            "subject": forms.Select(attrs={"class": "form-select"}),
            "teacher": forms.Select(attrs={"class": "form-select"}),
            "department": forms.Select(attrs={"class": "form-select"}),
            "session": forms.Select(attrs={"class": "form-select"}),
            "student_class": forms.Select(attrs={"class": "form-select"}),
            "section": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }