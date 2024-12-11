from decimal import Decimal
from django.db import models
from real_estate_manager.finance.models import Income  # Import Income model

class Tenant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_info = models.TextField()
    property = models.ForeignKey('properties.Property', related_name="tenants", on_delete=models.CASCADE)
    lease_start_date = models.DateField()
    lease_end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    rent_duration = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='tenant_photos/', null=True, blank=True)
    owner = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """Override save to automatically calculate rent_duration if not provided and create income record."""
        if not self.rent_duration:
            lease_duration = self.lease_end_date - self.lease_start_date
            self.rent_duration = lease_duration.days / 30

        super().save(*args, **kwargs)

        self.create_income_record_if_not_exists()

    def create_income_record_if_not_exists(self):
        """Ensure income record is created for the tenant if it does not exist."""
        if not Income.objects.filter(tenant=self).exists():
            # Create income record for this tenant
            Income.create_income_for_tenant(self)

    def calculate_projected_income(self):
        """This method calculates the projected income based on lease duration."""
        lease_duration = self.lease_end_date - self.lease_start_date
        total_days = lease_duration.days

        daily_rent = Decimal(self.monthly_rent) / Decimal(30)  # Approximate daily rent for simplicity

        projected_income = daily_rent * Decimal(total_days)

        return projected_income.quantize(Decimal('0.01'))

    def update_income_records(self):
        """Recalculate and update all income records based on the new monthly rent or lease period."""
        income_records = Income.objects.filter(tenant=self)

        for income in income_records:
            income.amount = self.calculate_projected_income()
            income.save()