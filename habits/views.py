from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from habits.models import Habit, Place
from habits.paginators import CustomPagination
from habits.serializers import HabitSerializer, PlaceSerializer
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    """Вьюсет для реализации CRUD привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Метод perform_create из Django REST Framework (DRF),
        предназначенный для кастомизации процесса создания объектов через API."""
        habit = serializer.save()  # создаёт объект Course из валидных данных
        habit.owner = self.request.user  # Привязывает текущего пользователя к полю owner
        habit.save()  # Сохраняет объект с обновлёнными данными

    def get_permissions(self):
        if self.action in ["update", "partial_update", "retrieve", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        """Переопределяем queryset для фильтрации по текущему пользователю"""
        return super().get_queryset().filter(owner=self.request.user)


class PublicHabitViewSet(ReadOnlyModelViewSet):
    """Вьюсет для просмотра публичных привычек без авторизации"""

    serializer_class = HabitSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]  # Доступ без авторизации

    def get_queryset(self):
        """Все публичные привычки всех пользователей"""
        return Habit.objects.filter(is_published=True)


class PlaceCreateApiView(CreateAPIView):
    """Дженерик для создания места"""

    serializer_class = PlaceSerializer
    permission_classes = (IsAuthenticated,)


class PlaceListAPIview(ListAPIView):
    """Дженерик для просмотра списка мест"""

    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (IsAuthenticated,)
