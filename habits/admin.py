from django.contrib import admin

from habits.models import Habit, Place


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Класс администрирования позволяет контролировать отображение и поведение модели Habit
    в интерфейсе администратора"""

    # какие поля будут показаны в списке объектов
    list_display = (
        "id",
        "place",
        "action",
        "execution_time",
        "is_pleasant",
        "reward",
        "is_published",
    )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """Класс администрирования позволяет контролировать отображение и поведение модели Habit
    в интерфейсе администратора"""

    # какие поля будут показаны в списке объектов
    list_display = (
        "id",
        "name",
        "description",
    )
