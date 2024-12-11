from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from decimal import Decimal
from django.utils import timezone

from real_estate_manager.properties.models import Property


class PropertyModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )

        self.property = Property.objects.create(
            name="Test Property",
            address="123 Test St",
            property_type="House",
            size=Decimal('150.00'),
            purchase_date=timezone.now().date(),
            value=Decimal('500000.00'),
            owner=self.user,
            image=None
        )

    def test_property_creation(self):
        """Test that a property can be created with valid data."""
        self.assertEqual(self.property.name, "Test Property")
        self.assertEqual(self.property.address, "123 Test St")
        self.assertEqual(self.property.property_type, "House")
        self.assertEqual(self.property.size, Decimal('150.00'))
        self.assertEqual(self.property.purchase_date, self.property.purchase_date)
        self.assertEqual(self.property.value, Decimal('500000.00'))
        self.assertEqual(self.property.owner, self.user)

    def test_property_str_method(self):
        """Test the string representation of the Property model."""
        self.assertEqual(str(self.property), "Test Property (House)")

    def test_valid_property_types(self):
        """Test that only valid property types are accepted."""
        valid_types = ['Condo', 'Apartment', 'House']
        for property_type in valid_types:
            property_instance = Property(
                name="Valid Property",
                address="123 Valid St",
                property_type=property_type,
                size=Decimal('100.00'),
                purchase_date=timezone.now().date(),
                value=Decimal('200000.00'),
                owner=self.user
            )
            property_instance.save()
            self.assertEqual(property_instance.property_type, property_type)

    def test_invalid_property_type(self):
        """Test that invalid property types raise a ValidationError."""
        with self.assertRaises(ValidationError):
            property_instance = Property(
                name="Invalid Property",
                address="123 Invalid St",
                property_type="InvalidType",
                size=Decimal('100.00'),
                purchase_date=timezone.now().date(),
                value=Decimal('200000.00'),
                owner=self.user
            )
            property_instance.full_clean()
            property_instance.save()

    def test_property_meta_options(self):
        """Test that the meta options verbose_name and verbose_name_plural are set correctly."""
        self.assertEqual(str(Property._meta.verbose_name), "Property")
        self.assertEqual(str(Property._meta.verbose_name_plural), "Properties")

    def test_foreign_key_relationship_with_user(self):
        """Test the ForeignKey relationship between Property and User."""
        self.assertEqual(self.property.owner, self.user)
        self.assertIn(self.property, self.user.properties.all())
