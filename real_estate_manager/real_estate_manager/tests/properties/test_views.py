from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model  # Import get_user_model
from real_estate_manager.properties.models import Property
from decimal import Decimal
from django.utils import timezone

class PropertyCreateViewTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username='testuser', password='password123')

    def test_property_creation(self):
        """Test property creation view works."""
        self.client.login(username='testuser', password='password123')
        url = reverse('create_property')
        data = {
            'name': 'Test Property',
            'address': '123 Test Street',
            'property_type': 'House',
            'size': Decimal('150.00'),
            'purchase_date': timezone.now().date(),
            'value': Decimal('300000.00'),
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Property.objects.filter(name='Test Property').exists())

    def test_property_creation_invalid_data(self):
        """Test property creation with missing required fields returns validation errors."""
        self.client.login(username='testuser', password='password123')
        url = reverse('create_property')
        data = {
            'name': '',
            'address': '123 Test Street',
            'property_type': 'House',
            'size': Decimal('150.00'),
            'purchase_date': timezone.now().date(),
            'value': Decimal('300000.00'),
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))
        self.assertIn('This field is required.', form.errors['name'])