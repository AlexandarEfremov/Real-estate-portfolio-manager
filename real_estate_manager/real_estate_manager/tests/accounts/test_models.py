from django.test import TestCase
from real_estate_manager.accounts.models import CustomUser


class CustomUserModelTests(TestCase):

    def test_create_user_with_valid_data(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            user_type='regular_user',
        )
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.user_type, 'regular_user')

    def test_user_string_representation(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
        )
        self.assertEqual(str(user), 'testuser@example.com')


if __name__ == "__main__":
    import unittest
    unittest.main()
