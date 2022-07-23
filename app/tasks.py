import datetime
import requests

from celery import shared_task
from django.conf import settings

from app.views import get_sheet_as_list, sync_rows_and_orders
from app.models import Order


@shared_task
def sync_sheet_and_db():
    rows = get_sheet_as_list()
    sync_rows_and_orders(rows)


@shared_task
def notify_telegram():
    today = datetime.date.today()
    overdue_orders = Order.objects.filter(order_date__lte=today, notified=False)
    text = ''
    for order in overdue_orders:
        text += f'Уведомление о просроченном заказе № {order.id}\n'
    if not text:
        return
    overdue_orders.update(notified=True)
    response = requests.post(
        f'https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage',
        data={
            'chat_id': settings.CHAT_ID,
            'text': text
        }
    )
    return response.json()
