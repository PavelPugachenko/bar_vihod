from datetime import date
from datetime import time as dt_time
import json
import logging
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)


def send_reservation_to_telegram(
    *,
    name: str,
    phone: str,
    reservation_date: date,
    reservation_time: dt_time,
) -> tuple[bool, str]:
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not bot_token or not chat_id:
        return False, "Telegram не настроен: добавьте TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID."

    message = (
        "Новая бронь с сайта\n"
        f"Имя: {name}\n"
        f"Телефон: {phone}\n"
        f"Дата: {reservation_date:%d.%m.%Y}\n"
        f"Время: {reservation_time:%H:%M}\n"
        "Статус: Ожидает подтверждения менеджером"
    )

    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode("utf-8")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    request = urllib.request.Request(url=url, data=payload, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            body = response.read().decode("utf-8")
            data = json.loads(body)
            if bool(data.get("ok")):
                return True, ""
            return False, "Telegram API вернул ошибку, заявка не отправлена."
    except Exception as exc:  # pragma: no cover
        logger.warning("Failed to send reservation to Telegram: %s", exc)
        return False, "Ошибка отправки в Telegram. Попробуйте еще раз."
