from django.contrib import admin

from app.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'dollar_price', 'order_date')
