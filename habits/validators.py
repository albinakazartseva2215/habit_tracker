from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_periodicity(value):
    """
    Валидатор периодичности выполнения привычек
    - Для полезных привычек: 1-7 дней
    """
    if value < 1 or value > 7:
        raise ValidationError(
            _("Периодичность полезных привычек должна быть от 1 до 7 дней"),
            params={"value": value},
        )
