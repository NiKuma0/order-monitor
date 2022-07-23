from http import HTTPStatus
import httplib2
import datetime

from django.conf import settings
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from googleapiclient.discovery import build, Resource
from oauth2client.service_account import ServiceAccountCredentials

from app.models import Order
from app.serializers import OrderSerializer


def get_service() -> Resource:
    '''Получить доступ к Google таблице

    Returns:
        service: Объект для создания запросов в Google Sheets API
    '''
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        settings.CREDENTIALS_JSON_FILE, settings.SCOPES
    )
    creds.authorize
    if creds.invalid:
        if creds.refresh_token:
            creds.refresh(httplib2.Http())
        raise Exception('Неверный токен!')
    return build('sheets', 'v4', credentials=creds)


def sync_sheet_and_db(rows: list[list]) -> int:
    '''Синхронизация ДБ с таблицей

    Args:
        rows: Строки из таблицы в формате [[<id>, <order_id>, <order_date>],]
    Returns:
        count_created: Кол-во созданных заказов
    '''

    ids = [int(row[0]) for row in rows]
    orders_to_update = Order.objects.in_bulk(ids)
    orders_to_create = []

    for row in rows:
        if not (order := orders_to_update.get(int(row[0]), False)):
            order = Order()
            orders_to_create.append(order)
        order.id, order.order_id, order.dollar_price, order.order_date = row
        order.order_date = datetime.datetime.strptime(order.order_date, '%d.%m.%Y')

    with transaction.atomic():
        Order.objects.exclude(id__in=ids).delete()
        Order.objects.bulk_update(
            orders_to_update.values(), fields=('order_id', 'dollar_price', 'order_date')
        )
        created = Order.objects.bulk_create(orders_to_create)
    return len(created)


def get_sheet_as_list():
    service = get_service()
    sheet: Resource = service.spreadsheets()
    data = sheet.values().get(
        spreadsheetId=settings.SHEET_ID,
        majorDimension='ROWS',
        range='A2:D999'
    ).execute()
    return data['values']


class OrderViewSet(GenericViewSet, ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(('PATH',), detail=False, url_path='import')
    def order_import(self):
        rows = get_sheet_as_list()
        count_created = sync_sheet_and_db(rows['values'])
        if not count_created:
            return Response(status=HTTPStatus.OK)
        return Response(
            {'count_created': count_created},
            status=HTTPStatus.CREATED
        )
