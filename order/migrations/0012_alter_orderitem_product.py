# Generated by Django 3.2.5 on 2021-08-19 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20210809_0003'),
        ('order', '0011_auto_20210818_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, help_text='select product for add to your Cart', null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='selected product'),
        ),
    ]