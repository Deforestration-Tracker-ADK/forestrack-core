from django import forms


class AcceptVolunteerOpportunity(forms.Form):
    approve = forms.BooleanField(required=True)
    vol_opp_id = forms.IntegerField(required=True)
