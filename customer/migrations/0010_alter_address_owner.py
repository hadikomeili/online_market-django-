# Generated by Django 3.2.5 on 2021-08-08 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_alter_address_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='owner',
            field=models.ForeignKey(help_text='specify customer', on_delete=django.db.models.deletion.PROTECT, to='customer.customer', verbose_name='customer name'),
        ),
    ]
