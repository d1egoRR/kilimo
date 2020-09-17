import datetime
import pytest

from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIClient

from app.models import FieldTerrain, Rain


@pytest.mark.django_db
class TestFieldTerrainViewSet:

    @pytest.fixture
    def client(self, db):
        return APIClient()

    @pytest.fixture
    def fieldterrain(self, db):
        return mixer.blend(FieldTerrain, name='Campo 1')

    @pytest.fixture
    def fieldterrain_with_rains(self, fieldterrain, db):
        curren_datetime = datetime.datetime.now()
        mixer.blend(
            Rain,
            fieldterrain=fieldterrain,
            rain_date=(curren_datetime - datetime.timedelta(days=1)).date(),
            milimeters=55
        )
        mixer.blend(
            Rain,
            fieldterrain=fieldterrain,
            rain_date=(curren_datetime - datetime.timedelta(days=2)).date(),
            milimeters=120
        )
        mixer.blend(
            Rain,
            fieldterrain=fieldterrain,
            rain_date=(curren_datetime - datetime.timedelta(days=5)).date(),
            milimeters=120
        )
        return fieldterrain

    def test_fieldterrain_list(self, client, fieldterrain):
        response = client.get(reverse('fieldterrain-list'))
        assert response.json is not None
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]['name'] == fieldterrain.name

    def test_fieldterrain_rains_list(self, client, fieldterrain_with_rains):
        response = client.get(
            reverse(
                'fieldterrain-rains',
                kwargs={'uuid': fieldterrain_with_rains.uuid}
            )
        )
        assert response.json is not None
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3

    def test_average_rain(self, client, fieldterrain_with_rains):
        response = client.get(
            reverse('fieldterrain-average-rain', kwargs={'days':2})
        )
        assert response.json is not None
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['average_rain'] == 87.5

        response = client.get(
            reverse('fieldterrain-average-rain', kwargs={'days':7})
        )
        assert response.json is not None
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['average_rain'] == 98.33

        # Tope de dias == 7 -> Bad Request
        response = client.get(
            reverse('fieldterrain-average-rain', kwargs={'days':10})
        )
        assert response.json is not None
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.json()

    def test_cumulative_rain_greater_than(self, client, fieldterrain_with_rains):
        response = client.get(
            reverse(
                'fieldterrain-cumulative-rain-greater-than',
                kwargs={'milimeters':200}
            )
        )
        assert response.json is not None
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

        response = client.get(
            reverse(
                'fieldterrain-cumulative-rain-greater-than',
                kwargs={'milimeters':1500}
            )
        )
        assert response.json is not None
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0


@pytest.mark.django_db
class TestRainViewSet:

    @pytest.fixture
    def client(self, db):
        return APIClient()

    @pytest.fixture
    def rain(self, db):
        return mixer.blend(Rain, rain_date='2020-09-07')

    def test_rain_list(self, client, rain):
        response = client.get(reverse('rain-list'))
        assert response.json is not None
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['rain_date'] == str(rain.rain_date)
