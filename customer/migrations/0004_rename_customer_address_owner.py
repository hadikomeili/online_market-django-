# Generated by Django 3.2.5 on 2021-08-06 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_address_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='customer',
            new_name='owner',
        ),
    ]
