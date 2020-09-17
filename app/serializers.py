from rest_framework import serializers

from .models import FieldTerrain, Rain


class FieldTerrainSerializer(serializers.ModelSerializer):
    average_rain = serializers.SerializerMethodField()

    def get_average_rain(self, obj):
        days = self.context.get('days', None)
        if days is not None:
            return obj.average_rain(days)

    class Meta:
        model = FieldTerrain
        fields = "__all__"


class RainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rain
        fields = "__all__"
