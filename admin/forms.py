from django import forms

from authentication.enums import UserType


class ApproveForm(forms.Form):
    approve = forms.BooleanField(required=True)
    id = forms.IntegerField(required=True)
    user_type = forms.ChoiceField(choices=UserType.choices, required=False)
