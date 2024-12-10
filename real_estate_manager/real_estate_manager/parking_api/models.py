from django.conf import settings
from django.db import models

from real_estate_manager.properties.models import Property
from real_estate_manager.tenants.models import Tenant


class ParkingSpace(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Occupied', 'Occupied'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='parking_spaces',
        help_text="The property to which this parking space belongs."
    )
    identifier = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique identifier for the parking space (e.g., Spot A1, Garage #3)."
    )
    size = models.CharField(
        max_length=50,
        help_text="Size description of the parking space (e.g., Compact, Standard, Large)."
    )
    is_covered = models.BooleanField(
        default=False,
        help_text="Indicates if the parking space is covered."
    )
    monthly_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Monthly rent amount for the parking space."
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available',
        help_text="Current status of the parking space."
    )
    tenant = models.ForeignKey(
        Tenant,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='parking_spaces',
        help_text="The tenant who has rented this parking space, if any."
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # This will point to the User model
        on_delete=models.CASCADE,
        related_name='parking_spaces',
        help_text="The owner of this parking space."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Parking Space {self.identifier} - {self.property.name}"

    class Meta:
        verbose_name = "Parking Space"
        verbose_name_plural = "Parking Spaces"
        unique_together = ('property', 'identifier')

