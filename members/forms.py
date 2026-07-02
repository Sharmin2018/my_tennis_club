from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'name',
            'roll',
            'registration_no',
            'session',
            'student_class',
            'email',
            'phone',
            'dob',
            'religion',
            'gender',
            'photo',
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

            'session': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter session'
            }),

            'student_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter class'
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

            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }