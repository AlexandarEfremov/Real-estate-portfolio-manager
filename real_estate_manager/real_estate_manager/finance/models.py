from django.db import models
from decimal import Decimal
from django.conf import settings
from real_estate_manager.properties.models import Property

class Income(models.Model):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, related_name="income_records")  # Use a string for deferred import
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="income_records")

    def __str__(self):
        return f"{self.amount} - {self.tenant.first_name} {self.tenant.last_name} ({self.date})"

    @property
    def projected_income(self):
        """
        Calculate the projected income based on the tenant's lease.
        This is calculated dynamically when accessed.
        """
        from real_estate_manager.tenants.models import Tenant  # Import inside method to avoid circular import
        if self.tenant.lease_start_date and self.tenant.lease_end_date:
            lease_duration = self.tenant.lease_end_date - self.tenant.lease_start_date
            total_days = lease_duration.days
            if total_days > 0:
                # Calculate daily rent by dividing the monthly rent by 30 (approx. days)
                daily_rent = self.tenant.monthly_rent / Decimal(30)  # Using 30 days for simplicity
                projected_income = daily_rent * Decimal(total_days)  # Total projected income
                return projected_income.quantize(Decimal('0.01'))  # Ensure 2 decimal places
        return Decimal('0.00')

    def save(self, *args, **kwargs):
        """Override save method to automatically link user to the income record."""
        if not self.pk:  # If it's a new record
            self.user = self.tenant.owner  # Link the income record to the tenant's owner
        super().save(*args, **kwargs)

    @classmethod
    def create_income_for_tenant(cls, tenant):
        """
        Create an income record for the given tenant based on their projected income.
        """
        from real_estate_manager.tenants.models import Tenant  # Import inside method to avoid circular import
        projected_income = tenant.calculate_projected_income()  # Get the projected income value

        # Create the income record for this tenant with the calculated amount
        return cls.objects.create(
            tenant=tenant,
            amount=projected_income,  # Use the calculated projected income
            date=tenant.lease_start_date,  # Use the start date for income
            description=f"Projected rent for {tenant.first_name} {tenant.last_name}",
            user=tenant.owner  # Link the income record to the owner of the tenant
        )


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
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.SET_NULL, null=True, blank=True, related_name="expense_records")  # Use string here too
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expense_records")

    def __str__(self):
        return f"{self.category}: {self.amount} - {self.property.name} ({self.date})"
