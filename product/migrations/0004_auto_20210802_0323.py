# Generated by Django 3.2.5 on 2021-08-01 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expire_time',
            field=models.DateField(help_text='specify expire time', verbose_name='discount expire time'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='start_time',
            field=models.DateField(help_text='specify start time', verbose_name='discount start time'),
        ),
    ]
