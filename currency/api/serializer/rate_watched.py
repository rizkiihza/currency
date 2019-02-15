from rest_framework import serializers
from django.apps import apps

RateWatched = apps.get_model("currency_processor", "RateWatched")

class RateWatchedSerializer(serializers.ModelSerializer):
    class Meta:
        model=RateWatched

        fields=(
            "user",
            "currency_from",
            "currency_to"
        )