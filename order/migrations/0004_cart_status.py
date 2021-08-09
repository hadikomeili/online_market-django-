# Generated by Django 3.2.5 on 2021-08-09 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_orderitem_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('WA', 'waiting'), ('FI', 'final cart')], default='W', help_text='display cart status', max_length=20, verbose_name='cart status'),
        ),
    ]