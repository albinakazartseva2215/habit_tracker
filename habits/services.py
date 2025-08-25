import requests

from config import settings
import logging

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    """Функция отправки сообщения в телеграм"""

    try:
        url = f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage"
        params = {"chat_id": chat_id, "text": message}
        requests.get(url, params=params)
    except requests.RequestException as e:
        logger.error(f"Telegram API error: {e}")
