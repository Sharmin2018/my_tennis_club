from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            # Academic
             "roll",
             "registration_no",
             "session",
            "student_class",
            "section",
            "department",

            # Student
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
            "email",
            "phone",
            "present_address",
            "permanent_address",

            # Guardian
            "guardian_name",
            "guardian_phone",
            "guardian_occupation",

            # Photo
            "photo",
        ]


        

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student name'
            }),

            'roll': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter roll number'
            }),

            'registration_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter registration number'
            }),

            "session": forms.Select(attrs={
                "class": "form-select",
            }),

        
            "student_class": forms.Select(attrs={
             "class": "form-select",
            }),

            "section": forms.Select( attrs={
             "class": "form-select",
             }),

            "department": forms.Select(attrs={
                "class": "form-select"
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),

            'dob': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'religion': forms.Select(attrs={
                'class': 'form-select'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),

            "father_name": forms.TextInput(attrs={"class":"form-control"}),
            "mother_name": forms.TextInput(attrs={"class":"form-control"}),
            "nationality": forms.TextInput(attrs={"class":"form-control"}),
            "previous_school": forms.TextInput(attrs={"class":"form-control"}),

            "blood_group": forms.Select(attrs={"class":"form-select"}),

            "present_address": forms.Textarea(attrs={
                "rows":3,
                 "class":"form-control",
                }),

            "permanent_address": forms.Textarea(attrs={
                "rows":3,
                "class":"form-control",
                }),

            "guardian_name": forms.TextInput(attrs={"class":"form-control"}),
            "guardian_phone": forms.TextInput(attrs={"class":"form-control"}),
            "guardian_occupation": forms.TextInput(attrs={"class":"form-control"}),


            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


