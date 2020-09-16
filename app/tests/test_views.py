from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from app.models import FieldTerrain, Rain


class TestFieldTerrainViewSet(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.base_endpoint = '/api/app/v1'

    def test_fieldterrain_list(self):
        # create fieldterrains
        fieldterrain1 = mixer.blend(FieldTerrain, name='Campo 1')
        fieldterrain2 = mixer.blend(FieldTerrain, name='Campo 2')

        response = self.client.get(f'{self.base_endpoint}/fieldterrains/')

        assert response.json is not None
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]['name'] == fieldterrain1.name

    def test_rain_list(self):
        # create rains
        rain1 = mixer.blend(Rain, rain_date='2020-09-05')
        rain2 = mixer.blend(Rain, rain_date='2020-09-07')

        response = self.client.get(f'{self.base_endpoint}/rains/')

        assert response.json is not None
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[1]['rain_date'] == str(rain2.rain_date)
