# Generated by Django 3.2.5 on 2021-08-14 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210808_2320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='national_code',
        ),
    ]
