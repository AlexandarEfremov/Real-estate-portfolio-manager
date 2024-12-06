# Generated by Django 5.1.3 on 2024-12-03 20:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('category', models.CharField(choices=[('Maintenance', 'Maintenance'), ('Utilities', 'Utilities'), ('Tax', 'Tax'), ('Other', 'Other')], max_length=50)),
                ('description', models.TextField(blank=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_records', to='properties.property')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='income_records', to='properties.property')),
            ],
        ),
    ]
