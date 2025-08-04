from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from habits.validators import validate_periodicity


class Habit(models.Model):
    """Модель привычки с заданными полями и мета классом"""

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        verbose_name="Владелец привычки",
        help_text="Укажите владельца привычки",
        blank=True,
        null=True,
    )
    place = models.ForeignKey(
        "habits.Place",
        on_delete=models.SET_NULL,
        verbose_name="Место выполнения",
        blank=True,
        null=True,
        help_text="Выберите место выполнения привычки",
        related_name="habits",
    )
    execution_time = models.TimeField(
        verbose_name="Время выполнения",
        help_text="Введите время выполнения",
        blank=True,
        null=True,
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие привычки",
        blank=True,
        null=False,  # пустая строка вместо null
        default="",  # Устанавливаем пустую строку по умолчанию
        help_text="Конкретное действие, которое представляет привычка",
    )
    is_pleasant = models.BooleanField(
        verbose_name="Признак приятной привычки",
        default=False,
        help_text="Отметьте, если привычка приятная",
    )
    habit_related = models.ForeignKey(
        "habits.Habit",
        on_delete=models.SET_NULL,
        related_name="rewarded_habits",
        verbose_name="Связанная приятная привычка",
        help_text="Приятная привычка, связанная с выполнением этой привычки",
        blank=True,
        null=True,
        limit_choices_to={"is_pleasant": True},
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность в днях",
        help_text="Интервал в днях между выполнениями (от 1 до 7)",
        validators=[validate_periodicity],  # Применяем валидатор
    )
    reward = models.CharField(
        verbose_name="Вознаграждение",
        max_length=255,
        blank=True,
        null=True,
        help_text="Чем пользователь должен себя вознаградить после выполнения " "(альтернатива связанной привычке)",
    )
    time_required = models.PositiveIntegerField(
        verbose_name="Время на выполнение (секунды)",
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        help_text="Время в секундах, которое займет выполнение привычки (максимум 120 секунд)",
    )
    is_published = models.BooleanField(
        verbose_name="Признак публичности",
        default=False,
        help_text="Отметьте для публикации привычки в общий доступ",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return self.action

    def clean(self):
        """
        Валидация модели согласно бизнес-правилам:
        - Приятная привычка не может иметь вознаграждения или связанной привычки
        - Полезная привычка может иметь только один тип вознаграждения
        - Связанная привычка должна быть приятной
        - Запрет самоссылок
        """
        # Правило 1: Для приятных привычек
        if self.is_pleasant:
            errors = {}

            # Проверка связанной привычки
            if self.habit_related:
                errors["habit_related"] = "Приятная привычка не может иметь связанных привычек"

            # Проверка вознаграждения (учитываем пустую строку)
            if self.reward and self.reward.strip():
                errors["reward"] = "Приятная привычка не может иметь вознаграждения"

            if errors:
                raise ValidationError(errors)

        # Правило 2: Для полезных привычек
        else:
            # Проверка конфликта вознаграждений
            if self.habit_related and self.reward and self.reward.strip():
                raise ValidationError(
                    {
                        "habit_related": "Укажите либо связанную привычку, либо вознаграждение",
                        "reward": "Укажите либо связанную привычку, либо вознаграждение",
                    }
                )

            # Проверка типа связанной привычки
            if self.habit_related:
                # Защита от рекурсивных запросов при сохранении новой привычки
                try:
                    if not self.habit_related.is_pleasant:
                        raise ValidationError({"habit_related": "Связанная привычка должна быть приятной"})
                except Habit.DoesNotExist:
                    # Игнорируем если связанная привычка еще не сохранена
                    pass

        # Общие правила
        # 1. Запрет самоссылок
        if self.habit_related and self.habit_related_id == self.id:
            raise ValidationError({"habit_related": "Привычка не может быть связана сама с собой"})

        # 2. Проверка существования связанной привычки
        if self.habit_related_id and not Habit.objects.filter(pk=self.habit_related_id).exists():
            raise ValidationError({"habit_related": "Указанная связанная привычка не существует"})

        # Вызов родительской валидации
        super().clean()

    def save(self, *args, **kwargs):
        """Автоматическая очистка полей перед сохранением"""
        # Для приятных привычек очищаем недопустимые поля
        if self.is_pleasant:
            self.habit_related = None
            self.reward = None

        # Для полезных привычек очищаем вознаграждение если есть связанная привычка
        elif self.habit_related:
            self.reward = None

        self.full_clean()
        super().save(*args, **kwargs)


class Place(models.Model):
    """Модель места с заданными полями и мета классом"""

    name = models.CharField(
        max_length=255,
        verbose_name="Название места",
        unique=True,
        help_text="Уникальное название места (например: Дом, Офис, Спортзал)",
    )
    description = models.TextField(
        verbose_name="Описание места", blank=True, null=True, help_text="Дополнительная информация о месте"
    )

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.name
