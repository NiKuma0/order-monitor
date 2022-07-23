from django.db import models


class Order(models.Model):
    id = models.IntegerField('№', primary_key=True)
    order_id = models.IntegerField('заказ №',)
    dollar_price = models.IntegerField('Стоимость $')
    order_date = models.DateField('Срок поставки')
    notified = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)
