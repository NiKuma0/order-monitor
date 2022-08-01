import httplib2
import datetime

from django.db import transaction
from googleapiclient.discovery import build, Resource
from oauth2client.service_account import ServiceAccountCredentials

from app.models import Order


class GoogleSheet:
    def __init__(self, credentials_json_file, sheet_id, scopes):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_json_file, scopes
        )
        self.sheet_id = sheet_id
        self.scopes = scopes

    @property
    def service(self) -> Resource:
        '''service: Объект для создания запросов в Google Sheets API'''
        self.credentials.authorize(httplib2.Http())
        if self.credentials.invalid:
            if self.credentials.refresh_token:
                self.credentials.refresh(httplib2.Http())
            raise Exception('Неверный токен!')
        return build('sheets', 'v4', credentials=self.credentials)

    def as_list(self) -> list[list[str]]:
        sheet = self.service.spreadsheets()
        data = sheet.values().get(
            spreadsheetId=self.sheet_id,
            majorDimension='ROWS',
            range='A2:D999'
        ).execute()
        return data['values']


def sync_sheet_and_db(google_sheet: GoogleSheet | list[list[str]]) -> int:
    '''Синхронизация ДБ с таблицей

    Args:
        rows: Строки из таблицы в формате [[<id>, <order_id>, <order_date>],]
    Returns:
        count_created: Кол-во созданных заказов
    '''
    rows = google_sheet.as_list() if isinstance(google_sheet, GoogleSheet) else google_sheet
    ids = [int(row[0]) for row in rows]
    orders_to_update = Order.objects.in_bulk(ids)
    orders_to_create = []

    for row in rows:
        if not (order := orders_to_update.get(int(row[0]), False)):
            order = Order()
            orders_to_create.append(order)
        order.id, order.order_id, order.dollar_price, order.order_date = row
        order.order_date = datetime.datetime.strptime(order.order_date, '%d.%m.%Y')
        order.notified = False

    with transaction.atomic():
        Order.objects.exclude(id__in=ids).delete()
        Order.objects.bulk_update(
            orders_to_update.values(), fields=('order_id', 'dollar_price', 'order_date')
        )
        created = Order.objects.bulk_create(orders_to_create)
    return len(created)
