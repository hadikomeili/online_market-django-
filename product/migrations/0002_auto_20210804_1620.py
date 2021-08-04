# Generated by Django 3.2.5 on 2021-08-04 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='ref_category',
        ),
        migrations.AddField(
            model_name='category',
            name='ref_category',
            field=models.ManyToManyField(blank=True, null=True, related_name='_product_category_ref_category_+', to='product.Category'),
        ),
    ]
