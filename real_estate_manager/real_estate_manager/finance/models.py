from django.db import models
from django.conf import settings  # to refer to the custom user model
from real_estate_manager.properties.models import Property

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="income_records")
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="income_records")  # Add user relationship

    def __str__(self):
        return f"{self.amount} - {self.property.name} ({self.date})"

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Maintenance', 'Maintenance'),
        ('Utilities', 'Utilities'),
        ('Tax', 'Tax'),
        ('Other', 'Other'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="expense_records")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expense_records")  # Add user relationship

    def __str__(self):
        return f"{self.category}: {self.amount} - {self.property.name} ({self.date})"
