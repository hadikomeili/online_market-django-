# Generated by Django 3.2.5 on 2021-08-20 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0014_alter_address_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=models.FloatField(blank=True, help_text='enter/change latitude', null=True, verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=models.FloatField(blank=True, help_text='enter/change longitude', null=True, verbose_name='longitude'),
        ),
        migrations.AlterField(
            model_name='address',
            name='rest_of_address',
            field=models.TextField(blank=True, help_text='enter/change rest of address', verbose_name='rest of address'),
        ),
    ]
