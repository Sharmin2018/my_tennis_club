from django import forms
from .models import AdmissionApplication


class AdmissionApplicationForm(forms.ModelForm):

    class Meta:
        model = AdmissionApplication

        fields = [
            # Admission Information
            "admission_session",
            "student_class",
            "section",
            "department",

            # Student Information
            "name",
            "father_name",
            "mother_name",
            "dob",
            "gender",
            "religion",
            "blood_group",
            "nationality",
            "previous_school",

            # Contact
            "phone",
            "email",
            "present_address",
            "permanent_address",

            # Guardian
            "guardian_name",
            "guardian_phone",
            "guardian_occupation",

            # Documents
            "photo",
            "birth_certificate",
        ]

        widgets = {

            "dob": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "present_address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                }
            ),

            "permanent_address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            if not isinstance(field.widget, forms.Textarea):

                field.widget.attrs["class"] = "form-control"