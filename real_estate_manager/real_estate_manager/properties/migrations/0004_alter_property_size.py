# Generated by Django 5.1.3 on 2024-12-03 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_property_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='size',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Size (m²)'),
        ),
    ]
