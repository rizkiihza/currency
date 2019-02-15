from rest_framework import serializers
from django.apps import apps

Rate = apps.get_model("currency_processor", "Rate")

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rate

        fields = (
            "currency_from",
            "currency_to",
            "value",
            "date",
        )