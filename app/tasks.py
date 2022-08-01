import datetime
import requests

from celery import shared_task
from django.conf import settings

from app.google_sheet import GoogleSheet, sync_sheet_and_db
from app.models import Order


@shared_task
def task_sync_sheet_and_db():
    google_sheet = GoogleSheet(
        settings.CREDENTIALS_JSON_FILE, settings.SHEET_ID, settings.SCOPES
    )
    sync_sheet_and_db(google_sheet)


@shared_task
def notify_telegram():
    today = datetime.date.today()
    overdue_orders = Order.objects.filter(order_date__lte=today, notified=False)
    if not overdue_orders:
        return

    text = ''
    for order in overdue_orders:
        text += f'Уведомление о просроченном заказе № {order.id}\n'
    response = requests.post(
        f'https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage',
        data={
            'chat_id': settings.CHAT_ID,
            'text': text
        }
    )
    overdue_orders.update(notified=True)
    return response.json()
