from django.db import models
from django.conf import settings

class Property(models.Model):
    PROPERTY_TYPES = [
        ('Condo', 'Condo'),
        ('Apartment', 'Apartment'),
        ('House', 'House'),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    size = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Size (m²)")
    purchase_date = models.DateField()
    value = models.DecimalField(max_digits=12, decimal_places=2)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    image = models.ImageField(upload_to="property_images/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.property_type})"

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
