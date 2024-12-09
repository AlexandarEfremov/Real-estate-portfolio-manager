from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('regular_user', 'Regular User'),
    ]

    user_type = models.CharField(
        max_length=50,
        choices=USER_TYPE_CHOICES,
        default='regular_user',
        help_text='Please adjust the User Type before assigning permissions (e.g., Admin, Staff, or Regular User).'
    )

    def __str__(self):
        return self.email
