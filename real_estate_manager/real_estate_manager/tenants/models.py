from django.db import models
from real_estate_manager.properties.models import Property
from django.contrib.auth import get_user_model




class Tenant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_info = models.JSONField()  # Can store email, phone number, etc.
    property = models.ForeignKey(Property, related_name="tenants", on_delete=models.CASCADE)
    lease_start_date = models.DateField()
    lease_end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
