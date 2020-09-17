
import json

from django.shortcuts import get_list_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import FieldTerrain, Rain
from .serializers import FieldTerrainSerializer, RainSerializer


class FieldTerrainViewSet(viewsets.ModelViewSet):
    serializer_class = FieldTerrainSerializer
    queryset = FieldTerrain.objects.all()
    #permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ('get', 'post')
    lookup_field = 'uuid'

    @action(detail=True, methods=["GET"], name="Get Rains by FieldTerrain")
    def rains(self, request, *args, **kwargs):
        rain_list = get_list_or_404(
            Rain, fieldterrain__uuid=kwargs.get(self.lookup_field)
        )
        serializer = RainSerializer(rain_list, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path='average-rain/(?P<days>[^/.]+)',
        name="Get FieldTerrains with Average Rain in 'x' days"
    )
    def average_rain(self, request, days, *args, **kwargs):
        if int(days) not in range(1, 8):
            return Response(
                {'error': 'Invalid day param. Must be between 1 and 7'},
                status=status.HTTP_400_BAD_REQUEST
            )

        fieldterrain_list = get_list_or_404(FieldTerrain)
        serializer = FieldTerrainSerializer(
            fieldterrain_list,
            many=True,
            context={
                'days': int(days)
            }
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path='cumulative-rain-greater-than/(?P<milimeters>[^/.]+)',
        name="Get FieldTerrain with Acumulation Rain"
    )
    def cumulative_rain_greater_than(self, request, milimeters, *args, **kwargs):
        fieldterrain_list = [
            fieldterrain
            for fieldterrain in self.get_queryset()
            if fieldterrain.cumulative_rain_greater_than(milimeters)
        ]

        serializer = FieldTerrainSerializer(fieldterrain_list, many=True)
        return Response(serializer.data)


class RainViewSet(viewsets.ModelViewSet):
    serializer_class = RainSerializer
    queryset = Rain.objects.all()
    #permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ('get', 'post')
    lookup_field = 'uuid'
