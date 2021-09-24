from django.db import transaction
from rest_framework import serializers

from opportunity.models import Opportunity, VolunteerOpportunity
from vio.models import Vio
from volunteer.models import Volunteer


class OpportunitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, min_length=4, required=True)
    description = serializers.CharField(max_length=255, min_length=4, required=True)
    address = serializers.CharField(max_length=255, min_length=4)
    district = serializers.CharField(max_length=255, min_length=4, required=True)
    vio_id = serializers.IntegerField()

    class Meta:
        model = Opportunity
        fields = ('id', 'vio_id', 'name', 'description', 'address', 'district')

    def validate(self, attrs):
        if not Vio.objects.filter(user_id=attrs["vio_id"]).exists():
            raise serializers.ValidationError({"vio_id": "There is no VIO authentication error"})

        return super().validate(attrs)

    @transaction.atomic()
    def create(self, validated_data):
        vio = Vio.objects.get(user_id=validated_data["vio_id"])
        validated_data['vio'] = vio

        opportunity = Opportunity.objects.create(**validated_data)
        return opportunity


class ApplyForOpportunitySerializer(serializers.ModelSerializer):
    volunteer_id = serializers.IntegerField(required=True)
    opportunity_id = serializers.IntegerField(required=True)

    class Meta:
        model = VolunteerOpportunity
        fields = ('volunteer_id', 'opportunity_id')

    def validate(self, attrs):
        if not Volunteer.objects.filter(user_id=attrs["volunteer_id"]).exists():
            raise serializers.ValidationError({"volunteer_id": "No Volunteer with this volunteer Id"})

        if not Opportunity.objects.filter(id=attrs["opportunity_id"]).exists():
            raise serializers.ValidationError({"opportunity_id": "No Opportunity with this opportunity Id"})

        if VolunteerOpportunity.objects.filter(opportunity_id=attrs["opportunity_id"],
                                               volunteer_id=attrs["volunteer_id"]):
            raise serializers.ValidationError({"message": "volunteer has already applied to this opportunity"})

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        volunteer = Volunteer.objects.get(user_id=validated_data["volunteer_id"])
        opportunity = Opportunity.objects.get(id=validated_data["opportunity_id"])
        validated_data["opportunity"] = opportunity
        validated_data["volunteer"] = volunteer

        return VolunteerOpportunity.objects.create(**validated_data)
