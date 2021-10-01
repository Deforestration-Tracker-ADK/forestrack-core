from django import forms

from report.models import ReportPhoto


class ReportForm(forms.Form):
    district = forms.CharField(required=True, max_length=50)
    severity = forms.IntegerField(required=True)
    recent = forms.CharField(required=True, max_length=750)
    action_description = forms.CharField(required=True, max_length=750)
    special_notes = forms.CharField(required=True, max_length=750)


class ReportPhotoForm(forms.ModelForm):
    class Meta:
        model = ReportPhoto
        fields = ("image",)
