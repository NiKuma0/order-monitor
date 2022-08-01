from http import HTTPStatus

from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from app.models import Order
from app.serializers import OrderSerializer
from app.google_sheet import GoogleSheet, sync_sheet_and_db


class OrderViewSet(GenericViewSet, ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(('PATH',), detail=False, url_path='sync')
    def sync(self):
        google_sheet = GoogleSheet(
            settings.CREDENTIALS_JSON_FILE, settings.SHEET_ID, settings.SCOPES
        )
        count_created = sync_sheet_and_db(google_sheet.as_list())
        if not count_created:
            return Response(status=HTTPStatus.OK)
        return Response(
            {'count_created': count_created},
            status=HTTPStatus.CREATED
        )
