from django import forms
from django.core.exceptions import ValidationError

from .models import Subject, SubjectAssignment


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject

        fields = [
            "name",
            "code",
            "department",
            "student_class",
            "full_marks",
            "pass_marks",
            "credit",
            "is_optional",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter subject name",
                }
            ),

            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter unique subject code",
                }
            ),

            "department": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "student_class": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "full_marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "pass_marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "credit": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "is_optional": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    # =====================================================
    # SUBJECT NAME
    # =====================================================

    def clean_name(self):

        name = self.cleaned_data.get("name")

        if not name:
            raise ValidationError(
                "Subject name cannot be empty."
            )

        return name.strip()

    # =====================================================
    # SUBJECT CODE
    # =====================================================

    def clean_code(self):

        code = self.cleaned_data.get("code")

        if not code:
            raise ValidationError(
                "Subject code cannot be empty."
            )

        code = code.strip().upper()

        queryset = Subject.objects.filter(
            code__iexact=code
        )

        # Edit করার সময় নিজের record বাদ
        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():

            raise ValidationError(
                f"Subject code '{code}' already exists. "
                "Please use a different code."
            )

        return code

    # =====================================================
    # NAME + CLASS DUPLICATE CHECK
    # =====================================================

    def clean(self):

        cleaned_data = super().clean()

        name = cleaned_data.get("name")
        student_class = cleaned_data.get("student_class")

        if name and student_class:

            queryset = Subject.objects.filter(
                student_class=student_class,
                name__iexact=name.strip(),
            )

            # Edit করলে নিজের record বাদ
            if self.instance.pk:
                queryset = queryset.exclude(
                    pk=self.instance.pk
                )

            if queryset.exists():

                self.add_error(
                    "name",
                    f"Subject '{name}' already exists "
                    f"for {student_class}."
                )

        return cleaned_data


# =========================================================
# SUBJECT ASSIGNMENT FORM
# =========================================================

class SubjectAssignmentForm(forms.ModelForm):

    class Meta:

        model = SubjectAssignment

        fields = "__all__"

        widgets = {
            "subject": forms.Select(
                attrs={"class": "form-select"}
            ),

            "teacher": forms.Select(
                attrs={"class": "form-select"}
            ),

            "department": forms.Select(
                attrs={"class": "form-select"}
            ),

            "session": forms.Select(
                attrs={"class": "form-select"}
            ),

            "student_class": forms.Select(
                attrs={"class": "form-select"}
            ),

            "section": forms.Select(
                attrs={"class": "form-select"}
            ),

            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }