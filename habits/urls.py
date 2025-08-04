from django.urls import path
from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, PlaceCreateApiView, PlaceListAPIview, PublicHabitViewSet

app_name = HabitsConfig.name

router = SimpleRouter()
router.register("my-habits", HabitViewSet, basename="my-habits")
router.register("public-habits", PublicHabitViewSet, basename="public-habits")


urlpatterns = [
    path("places/create/", PlaceCreateApiView.as_view(), name="places-create"),
    path("places/", PlaceListAPIview.as_view(), name="places-list"),
]

urlpatterns += router.urls
