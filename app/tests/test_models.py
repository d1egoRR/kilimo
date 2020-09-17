import datetime

import pytest

from mixer.backend.django import mixer

from app.models import FieldTerrain, Rain


@pytest.mark.django_db
class TestFieldTerrain:

    @pytest.fixture
    def fieldterrain(self, db):
        fieldterrain = mixer.blend(FieldTerrain)

        curren_datetime = datetime.datetime.now()

        rain1 = mixer.blend(
            Rain,
            fieldterrain=fieldterrain,
            rain_date=(curren_datetime - datetime.timedelta(days=1)).date(),
            milimeters=55
        )
        rain2 = mixer.blend(
            Rain,
            fieldterrain=fieldterrain,
            rain_date=(curren_datetime - datetime.timedelta(days=2)).date(),
            milimeters=120
        )
        rain3 = mixer.blend(
            Rain,
            fieldterrain=fieldterrain,
            rain_date=(curren_datetime - datetime.timedelta(days=3)).date(),
            milimeters=75
        )
        return fieldterrain

    def test_average_rain(self, fieldterrain):
        assert fieldterrain.average_rain(days=0) is None
        assert fieldterrain.average_rain(days=2) == 87.5
        assert fieldterrain.average_rain(days=3) == 83.33

    def test_cumulative_rain_greater_than(self, fieldterrain):
        assert fieldterrain.cumulative_rain_greater_than(120) is True
        assert fieldterrain.cumulative_rain_greater_than(240) is True
        assert fieldterrain.cumulative_rain_greater_than(1000) is False
