# Generated by Django 3.2.5 on 2021-08-21 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_orderitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='order_status',
            field=models.CharField(choices=[('NW', 'new'), ('SN', 'send'), ('CA', 'cancel')], default='NW', help_text='display status of order', max_length=20, verbose_name='customer order status'),
        ),
    ]