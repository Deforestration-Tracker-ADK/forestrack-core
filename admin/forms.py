from rest_framework import serializers

from authentication.enums import UserType


class ApproveForm(serializers.Serializer):
    approve = serializers.BooleanField(required=True)
    id = serializers.IntegerField(required=True)
    user_type = serializers.ChoiceField(choices=UserType.choices, required=False)
