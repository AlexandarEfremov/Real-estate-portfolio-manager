from django.test import TestCase
from django.urls import reverse
from real_estate_manager.accounts.models import CustomUser


class ViewsTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password',
            email='testuser@example.com',
        )

    def test_custom_login_view_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'invaliduser',
            'password': 'invalidpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_registration_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'newuser@example.com',
        })
        self.assertContains(response, "Registration successful")

    def test_private_landing_page_requires_login(self):
        response = self.client.get(reverse('private_landing'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('private_landing')}")


if __name__ == "__main__":
    import unittest
    unittest.main()
