from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "password",
            "email",
        )