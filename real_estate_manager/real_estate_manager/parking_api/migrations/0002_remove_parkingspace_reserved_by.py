# Generated by Django 5.1.3 on 2024-12-10 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parkingspace',
            name='reserved_by',
        ),
    ]
