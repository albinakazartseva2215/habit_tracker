from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Класс предназначен для обработки запросов на создание нового пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # Создаёт экземпляр User из валидных данных, принудительно устанавливает is_active=True
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.is_active = True
        user.save()
