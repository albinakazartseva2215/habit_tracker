from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit, Place
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create(
            email="user@example.com",
        )
        self.other_user = User.objects.create(
            email="other@example.com",
        )

        # Создаем место
        self.place = Place.objects.create(name="Домашний офис", description="Мое рабочее место дома")

        # Создаем привычки для пользователя
        self.habit1 = Habit.objects.create(
            owner=self.user, place=self.place, action="Привычка 1", periodicity=1, time_required=60
        )

        self.habit2 = Habit.objects.create(
            owner=self.user, place=self.place, action="Привычка 2", periodicity=2, time_required=90, is_published=True
        )

        # Создаем привычку другого пользователя
        self.other_habit = Habit.objects.create(
            owner=self.other_user, place=self.place, action="Чужая привычка", periodicity=1, time_required=30
        )
        self.client.force_authenticate(user=self.user)
        self.client.force_authenticate(user=self.other_user)
        # URL для API
        self.list_url = reverse("habits:my-habits-list")
        self.detail_url = lambda pk: reverse("habits:my-habits-detail", args=[pk])

    def test_unauthenticated_list_access(self):
        """Неаутентифицированный пользователь не может получить список привычек"""
        # Выходим из системы перед тестом
        self.client.logout()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_list_access(self):
        """Аутентифицированный пользователь видит свои привычки"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # Используем пагинацию

        # Проверяем, что видим только свои привычки
        habit_ids = [habit["id"] for habit in response.data["results"]]
        self.assertIn(self.habit1.id, habit_ids)
        self.assertIn(self.habit2.id, habit_ids)
        self.assertNotIn(self.other_habit.id, habit_ids)

    # Тесты для получения деталей привычки
    def test_retrieve_own_habit(self):
        """Пользователь может получить детали своей привычки"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.habit1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.habit1.id)

    def test_retrieve_other_habit(self):
        """Пользователь не может получить детали чужой привычки"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url(self.other_habit.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Тесты для создания привычки
    def test_create_habit(self):
        """Пользователь может создать привычку"""
        self.client.force_authenticate(user=self.user)
        data = {"action": "Новая привычка", "place": self.place.id, "periodicity": 3, "time_required": 45}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что владелец установлен правильно
        habit = Habit.objects.get(id=response.data["id"])
        self.assertEqual(habit.owner, self.user)

    # Тесты для обновления привычки
    def test_update_own_habit(self):
        """Пользователь может обновить свою привычку"""
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.habit1.id)
        data = {"action": "Обновленная привычка"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit1.refresh_from_db()
        self.assertEqual(self.habit1.action, "Обновленная привычка")

    def test_update_other_habit(self):
        """Пользователь не может обновить чужую привычку"""
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.other_habit.id)
        data = {"action": "Несанкционированное обновление"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Тесты для удаления привычки
    def test_delete_own_habit(self):
        """Пользователь может удалить свою привычку"""
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.habit1.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit1.id).exists())

    def test_delete_other_habit(self):
        """Пользователь не может удалить чужую привычку"""
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.other_habit.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Habit.objects.filter(id=self.other_habit.id).exists())


class PublicHabitTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(
            email="user@example.com",
        )

        # Создаем место
        self.place = Place.objects.create(name="Парк")

        # Создаем публичные привычки
        self.public_habit1 = Habit.objects.create(
            owner=self.user,
            place=self.place,
            action="Публичная привычка 1",
            is_published=True,
            periodicity=1,
            time_required=60,
        )

        self.public_habit2 = Habit.objects.create(
            owner=self.user,
            place=self.place,
            action="Публичная привычка 2",
            is_published=True,
            periodicity=2,
            time_required=90,
        )

        # Создаем приватную привычку
        self.private_habit = Habit.objects.create(
            owner=self.user,
            place=self.place,
            action="Приватная привычка",
            is_published=False,
            periodicity=1,
            time_required=30,
        )

        # URL для API
        self.list_url = reverse("habits:public-habits-list")
        self.detail_url = lambda pk: reverse("habits:public-habits-detail", args=[pk])

    # Тесты для списка публичных привычек
    def test_unauthenticated_access_to_list(self):
        """Неаутентифицированный пользователь может получить список публичных привычек"""
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

        # Проверяем, что видны только публичные привычки
        habit_ids = [habit["id"] for habit in response.data["results"]]
        self.assertIn(self.public_habit1.id, habit_ids)
        self.assertIn(self.public_habit2.id, habit_ids)
        self.assertNotIn(self.private_habit.id, habit_ids)

    # Тест для деталей публичной привычки
    def test_access_to_private_habit_detail(self):
        """Нельзя получить детали приватной привычки через публичный эндпоинт"""
        response = self.client.get(self.detail_url(self.private_habit.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PlaceTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(
            email="user@example.com",
        )

        # Создаем несколько мест
        self.place1 = Place.objects.create(name="Дом")
        self.place2 = Place.objects.create(name="Офис")

        # URL для API
        self.place_list_url = reverse("habits:places-list")
        self.place_create_url = reverse("habits:places-create")

    def test_unauthenticated_access_to_place_list(self):
        """Неаутентифицированный пользователь не может получить список мест"""
        response = self.client.get(self.place_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_access_to_place_list(self):
        """Аутентифицированный пользователь может получить список мест"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.place_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_unauthenticated_access_to_place_create(self):
        """Неаутентифицированный пользователь не может создать место"""
        data = {"name": "Парк"}
        response = self.client.post(self.place_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_access_to_place_create(self):
        """Аутентифицированный пользователь может создать место"""
        self.client.force_authenticate(user=self.user)
        data = {"name": "Спортзал"}
        response = self.client.post(self.place_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что место создано
        self.assertTrue(Place.objects.filter(name="Спортзал").exists())

    def test_create_place_with_duplicate_name(self):
        """Нельзя создать место с неуникальным названием"""
        self.client.force_authenticate(user=self.user)
        data = {"name": "Дом"}  # Уже существует
        response = self.client.post(self.place_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
