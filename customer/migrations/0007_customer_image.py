# Generated by Django 3.2.5 on 2021-08-07 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_auto_20210807_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.FileField(blank=True, help_text='upload your image', null=True, upload_to='customer/images/', verbose_name='customer image'),
        ),
    ]
