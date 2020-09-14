import uuid

from datetime import datetime, timedelta

from django.db import models
from django.db.models import Avg, Q, Sum


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
        return round(result['milimeters__avg'], 2)

    def cumulative_rain_greater_than(self, milimeters):
        result = self.rains.aggregate(Sum('milimeters'))
        return result['milimeters__sum'] > milimeters

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Field Terrain"
        verbose_name_plural = "Field Terrains"


class Rain(models.Model):
    uuid = models.UUIDField(
        "UUID", default=uuid.uuid4, editable=False, unique=True
    )
    field_terrain = models.ForeignKey(
        FieldTerrain, on_delete=models.CASCADE, related_name='rains'
    )
    rain_date = models.DateField()
    milimeters = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return (f'{self.field_terrain} | {self.rain_date} | '
                f'{self.milimeters} milimeters')

    class Meta:
        verbose_name = "Rain"
        verbose_name_plural = "Rains"
