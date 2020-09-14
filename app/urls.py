from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import FieldTerrainViewSet, RainViewSet


router = SimpleRouter()
router.register(r"v1/fieldterrains", FieldTerrainViewSet)
router.register(r"v1/rains", RainViewSet)

urlpatterns = router.urls
