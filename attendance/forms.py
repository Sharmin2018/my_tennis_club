from django import forms

from academics.models import (
    Session,
    StudentClass,
    Section,
)

from departments.models import Department


from datetime import datetime


MONTH_CHOICES = [
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December"),
]



class AttendanceForm(forms.Form):

    session = forms.ModelChoiceField(
        queryset=Session.objects.all()
    )

    student_class = forms.ModelChoiceField(
        queryset=StudentClass.objects.all()
    )

    section = forms.ModelChoiceField(
        queryset=Section.objects.all()
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all()
    )

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        )
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs["class"] = "form-control"


class MonthlyReportForm(forms.Form):

    current_year = datetime.now().year

    year = forms.ChoiceField(
        choices=[
            (y, y)
            for y in range(current_year - 5, current_year + 6)
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    student_class = forms.ModelChoiceField(
        queryset=StudentClass.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )