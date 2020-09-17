import uuid

from datetime import datetime, timedelta

from django.db import models
from django.db.models import Avg, Sum


class FieldTerrain(models.Model):
    uuid = models.UUIDField(
        "UUID", default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=100)
    hectares = models.IntegerField()
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def average_rain(self, days):
        timestamp = datetime.now() - timedelta(days=days)
        result = self.rains.filter(
            rain_date__gte=timestamp.date()
        ).aggregate(
            Avg('milimeters')
        )
        if result['milimeters__avg'] is not None:
            return round(float(result['milimeters__avg']), 2)

    @classmethod
    def get_cumulative_rain_greater_than(self, milimeters):
        return FieldTerrain.objects.annotate(
            accumulated_milimeters=Sum('rains__milimeters')
        ).filter(
            accumulated_milimeters__gt=milimeters
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Field Terrain"
        verbose_name_plural = "Field Terrains"


class Rain(models.Model):
    uuid = models.UUIDField(
        "UUID", default=uuid.uuid4, editable=False, unique=True
    )
    fieldterrain = models.ForeignKey(
        FieldTerrain, on_delete=models.CASCADE, related_name='rains'
    )
    rain_date = models.DateField()
    milimeters = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return (f'{self.fieldterrain} | {self.rain_date} | '
                f'{self.milimeters} milimeters')

    class Meta:
        verbose_name = "Rain"
        verbose_name_plural = "Rains"
