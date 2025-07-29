from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс модели User"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Введите город",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        verbose_name="Аватарка",
        blank=True,
        null=True,
        help_text="Загрузите аватарку",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """Meta класс, который задает конфигурационные параметры"""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
