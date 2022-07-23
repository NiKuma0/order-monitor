import requests

from django.core.cache import cache
from rest_framework import serializers

from app.models import Order


def get_rub_rate():
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    value = data['Valute']['USD']['Value']
    return float(value)


class OrderSerializer(serializers.ModelSerializer):
    __rub_rate = None

    @property
    def rub_rate(self):
        if not self.__rub_rate:
            self.__rub_rate = cache.get_or_set('rub_rate', get_rub_rate)
        return self.__rub_rate

    order_date = serializers.DateField(
        format='%d.%m.%Y'
    )
    rub_price = serializers.SerializerMethodField()

    def get_rub_price(self, order: Order):
        return order.dollar_price * self.rub_rate

    class Meta:
        model = Order
        fields = (
            'id',
            'order_id',
            'dollar_price',
            'rub_price',
            'order_date',
        )
