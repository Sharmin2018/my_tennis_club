from django import forms
from .models import Notice


class NoticeForm(forms.ModelForm):

    class Meta:

        model = Notice

        exclude = (
            "created_by",
        )

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Notice Title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter Notice Description",
                }
            ),

            "publish_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "notice_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

        }