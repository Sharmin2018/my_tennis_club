from django import forms
from academics.models import StudentClass, Section


class PromotionForm(forms.Form):

    from_class = forms.ModelChoiceField(
        queryset=StudentClass.objects.all(),
        label="From Class"
    )

    from_section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        label="From Section"
    )

    to_class = forms.ModelChoiceField(
        queryset=StudentClass.objects.all(),
        label="To Class"
    )