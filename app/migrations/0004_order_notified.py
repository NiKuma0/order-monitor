# Generated by Django 4.0.6 on 2022-07-23 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_order_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notified',
            field=models.BooleanField(default=False),
        ),
    ]
