from django.contrib import admin

from .models import FieldTerrain, Rain


@admin.register(FieldTerrain)
class FieldTerrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'name', 'hectares', 'coords')
    search_fields = ('name',)

    def coords(self, instance):
        return (instance.latitude, instance.longitude)


@admin.register(Rain)
class RainAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'uuid', 'fieldterrain_name', 'rain_date', 'milimeters',
    )
    search_fields = ('fieldterrain__name',)
    list_filter = ('rain_date',)

    def fieldterrain_name(self, instance):
        return instance.fieldterrain.name
