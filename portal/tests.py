"""
Smoke tests for the City Hall portal.
Run: python manage.py test
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicPagesTests(TestCase):
    """Every public page must open without errors."""

    def test_home_page(self):
        response = self.client.get(reverse('portal:home'))
        self.assertEqual(response.status_code, 200)

    def test_laws_page(self):
        response = self.client.get(reverse('portal:laws'))
        self.assertEqual(response.status_code, 200)

    def test_business_page(self):
        response = self.client.get(reverse('portal:business'))
        self.assertEqual(response.status_code, 200)

    def test_business_filter_does_not_break(self):
        response = self.client.get(reverse('portal:business'), {'status': 'free', 'type': 'all'})
        self.assertEqual(response.status_code, 200)

    def test_employees_page(self):
        response = self.client.get(reverse('portal:employees'))
        self.assertEqual(response.status_code, 200)


class AuthTests(TestCase):
    """Login and admin access."""

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username='admin_test', email='admin@example.com', password='VeryStrongPass123'
        )

    def test_login_page_opens(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_admin_requires_login(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_admin_opens_for_superuser(self):
        self.client.force_login(self.user)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_notifications_requires_login(self):
        response = self.client.get(reverse('portal:notifications_api'))
        self.assertIn(response.status_code, (302, 403))
