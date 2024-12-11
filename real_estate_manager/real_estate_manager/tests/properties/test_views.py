from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model  # Import get_user_model
from real_estate_manager.properties.models import Property
from decimal import Decimal
from django.utils import timezone

class PropertyCreateViewTest(TestCase):
    def setUp(self):
        # Use the custom user model for creating a user
        self.User = get_user_model()  # Get the custom user model
        self.user = self.User.objects.create_user(username='testuser', password='password123')

    def test_property_creation(self):
        """Test property creation view works."""
        self.client.login(username='testuser', password='password123')
        url = reverse('create_property')  # Assuming 'property_create' is the URL name for PropertyCreateView
        data = {
            'name': 'Test Property',
            'address': '123 Test Street',
            'property_type': 'House',
            'size': Decimal('150.00'),
            'purchase_date': timezone.now().date(),
            'value': Decimal('300000.00'),
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # Expecting redirect after successful creation
        self.assertTrue(Property.objects.filter(name='Test Property').exists())  # Property should be created

    def test_property_creation_invalid_data(self):
        """Test property creation with missing required fields returns validation errors."""
        self.client.login(username='testuser', password='password123')
        url = reverse('create_property')
        data = {
            'name': '',  # Missing name, required field
            'address': '123 Test Street',
            'property_type': 'House',
            'size': Decimal('150.00'),
            'purchase_date': timezone.now().date(),
            'value': Decimal('300000.00'),
        }

        response = self.client.post(url, data)

        # Check that the response contains validation errors
        self.assertEqual(response.status_code, 200)  # Form should be re-rendered
        # Ensure the 'name' field has an error message indicating it is required
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))
        self.assertIn('This field is required.', form.errors['name'])