# Generated by Django 3.2.5 on 2021-08-14 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_alter_address_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='birthday',
            field=models.DateField(blank=True, help_text='specify birthday date', null=True, verbose_name='birthday'),
        ),
        migrations.AddField(
            model_name='customer',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], help_text='specify your gender', max_length=10, null=True, verbose_name='gender'),
        ),
        migrations.AddField(
            model_name='customer',
            name='national_code',
            field=models.CharField(blank=True, help_text='enter national code', max_length=10, null=True, verbose_name='national code'),
        ),
    ]
