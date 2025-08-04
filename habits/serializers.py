from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habits.models import Habit, Place
from habits.validators import validate_periodicity


class HabitSerializer(ModelSerializer):
    periodicity = serializers.IntegerField(
        min_value=1,
        max_value=7,
        help_text="Интервал в днях между выполнениями (1-7)",
        validators=[validate_periodicity],  # Применяем тот же валидатор
    )

    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        """Кастомная валидация"""
        # Проверяем периодичность
        periodicity = data.get("periodicity")
        if periodicity is not None:
            validate_periodicity(periodicity)

        return data


class PlaceSerializer(ModelSerializer):

    class Meta:
        model = Place
        fields = "__all__"
