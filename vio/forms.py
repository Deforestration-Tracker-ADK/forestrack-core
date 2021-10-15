from rest_framework import serializers


class AcceptVolunteerOpportunity(serializers.Serializer):
    approve = serializers.BooleanField(required=True)
    vol_opp_id = serializers.IntegerField(required=True)
