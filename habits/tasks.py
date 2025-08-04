from django.utils import timezone
from datetime import timedelta

from celery import shared_task

from habits.models import Habit
from habits.services import send_telegram_message
import logging

logger = logging.getLogger(__name__)


@shared_task(name="habits.tasks.remind_habit")
def remind_habit():
    """Отложенная функция напоминания о привычке"""
    try:
        now = timezone.localtime()
        start_time = now - timedelta(minutes=5)
        end_time = now + timedelta(minutes=5)

        habits = Habit.objects.filter(
            owner__isnull=False,
            execution_time__gte=start_time.time(),
            execution_time__lte=end_time.time(),
        )

        for habit in habits:
            if habit.owner and habit.owner.tg_chat_id:
                message = f"Напоминаю о привычке {habit.action}"
                send_telegram_message(habit.owner.tg_chat_id, message)

    except Exception as e:
        logger.error(f"Error in remind_habit task: {e}")
        raise

