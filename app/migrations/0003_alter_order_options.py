# Generated by Django 4.0.6 on 2022-07-21 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_order_id_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('id',)},
        ),
    ]
