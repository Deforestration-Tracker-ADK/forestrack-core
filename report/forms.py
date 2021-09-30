from django import forms

from report.models import ReportPhoto


class ReportForm(forms.Form):
    district = forms.CharField(required=False)
    severity = forms.IntegerField(required=False)
    recent = forms.BooleanField(required=True)
    action_description = forms.CharField(required=True, max_length=500)
    special_notes = forms.CharField(required=True, max_length=500)


class ReportPhotoForm(forms.ModelForm):
    class Meta:
        model = ReportPhoto
        fields = ("image",)
