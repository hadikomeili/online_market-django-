# Generated by Django 3.2.5 on 2021-08-16 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20210816_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='order_status',
            field=models.CharField(choices=[('NW', 'new'), ('IP', 'in process'), ('SN', 'send')], default='NW', help_text='display status of order', max_length=20, verbose_name='customer order status'),
        ),
    ]