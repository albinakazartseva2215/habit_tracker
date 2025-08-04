from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс администрирования позволяет контролировать отображение и поведение модели User
    в интерфейсе администратора"""

    # какие поля будут показаны в списке объектов
    list_display = (
        "id",
        "email",
    )
