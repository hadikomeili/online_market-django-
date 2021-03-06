# Generated by Django 3.2.5 on 2021-08-05 21:34

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0005_auto_20210806_0204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.user')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('core.user',),
            managers=[
                ('objects', core.models.MyUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modify_timestamp', models.DateTimeField(auto_now=True)),
                ('delete_timestamp', models.DateTimeField(blank=True, default=None, editable=False, null=True)),
                ('country', models.CharField(default='Iran', help_text='enter country name', max_length=30, verbose_name='country name')),
                ('state', models.CharField(help_text='enter state name', max_length=50, verbose_name='state name')),
                ('city', models.CharField(help_text='enter city name', max_length=50, verbose_name='city name')),
                ('village', models.CharField(blank=True, help_text='enter village name', max_length=50, null=True, verbose_name='village name')),
                ('rest_of_address', models.TextField(help_text='enter rest of address', verbose_name='rest of address')),
                ('post_code', models.CharField(blank=True, help_text='enter post code', max_length=10, null=True, verbose_name='post code')),
                ('customer', models.ForeignKey(help_text='specify customer', on_delete=django.db.models.deletion.CASCADE, to='customer.customer', verbose_name='customer name')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
