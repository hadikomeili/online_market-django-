# Generated by Django 3.2.5 on 2021-08-08 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20210808_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='cart',
            field=models.ForeignKey(blank=True, help_text='specify cart', null=True, on_delete=django.db.models.deletion.PROTECT, to='order.cart', verbose_name='cart'),
        ),
    ]
