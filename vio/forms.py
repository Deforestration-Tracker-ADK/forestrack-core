from django import forms


class AcceptVolunteerOpportunity(forms.Form):
    approve = forms.BooleanField(required=True)
    opportunity_id = forms.IntegerField(required=True)
    volunteer_id = forms.IntegerField(required=True)
