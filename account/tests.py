from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AccountViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.dashboard_url = reverse('dashboard')
        self.settings_url = reverse('user_settings')

    def test_user_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'wronguser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Wprowadź poprawne wartości pól')

    def test_user_login_valid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dashboard_url)

    def test_user_register_valid_data(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_dashboard_requires_login(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)

    def test_user_settings_authenticated_access(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/settings.html')