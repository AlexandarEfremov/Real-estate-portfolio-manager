# Generated by Django 5.1.3 on 2024-12-09 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('staff', 'Staff'), ('regular_user', 'Regular User')], default='regular_user', max_length=50),
        ),
    ]
