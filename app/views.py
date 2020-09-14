
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ('get', 'post')
    lookup_field = 'uuid'

    @action(detail=True, methods=["GET"], name="Get Rains by FieldTerrain")
    def rains(self, request, *args, **kwargs):
        rain_list = get_list_or_404(
            Rain, field_terrain__uuid=kwargs.get(self.lookup_field)
        )
        serializer = RainSerializer(rain_list, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        name="Get FieldTerrains with Rain Average"
    )
    def average_rain(self, request, *args, **kwargs):
        params = json.loads(request.body)
        days = params.get('days', None)

        if days not in range(1, 8):
            return Response(
                {'error': 'Invalid day param. Must be between 1 and 7'},
                status=status.HTTP_400_BAD_REQUEST
            )

        field_terrain_list = get_list_or_404(FieldTerrain)

        serializer = FieldTerrainSerializer(
            field_terrain_list,
            many=True,
            context={
                'days': params.get('days', None)
            }
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        name="Get FieldTerrain With Acumulation Rain"
    )
    def cumulative_rain_greater_than(self, request, *args, **kwargs):
        params = json.loads(request.body)
        milimeters = params.get('milimeters', None)

        if milimeters is None:
            return Response(
                {'error': 'Invalid param milimeters'},
                status=status.HTTP_400_BAD_REQUEST
            )

        field_terrain_list = [
            field_terrain
            for field_terrain in self.get_queryset()
            if field_terrain.cumulative_rain_greater_than(milimeters)
        ]

        serializer = FieldTerrainSerializer(field_terrain_list, many=True)
        return Response(serializer.data)


class RainViewSet(viewsets.ModelViewSet):
    serializer_class = RainSerializer
    queryset = Rain.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ('get', 'post')
    lookup_field = 'uuid'
