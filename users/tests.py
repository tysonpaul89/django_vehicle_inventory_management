"""Module to Unit test the user and superuser creation"""
from django.contrib.auth import get_user_model
from django.test import TestCase

class CustomUserTests(TestCase):

    def test_create_user(self):
        """Method to test user creation"""
        User = get_user_model()
        username = "Jack"
        email = "jack@mail.com"

        user = User.objects.create_user(
            username=username,
            email=email,
            password="pass@123"
        )

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Method to test super user creation"""
        User = get_user_model()
        username = "Jill"
        email = "jill@mail.com"

        admin = User.objects.create_superuser(
            username=username,
            email=email,
            password="pass@123"
        )

        self.assertEqual(admin.username, username)
        self.assertEqual(admin.email, email)
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_superuser)