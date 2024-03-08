from django.test import TestCase
from django.urls import reverse

class LoginTestCase(TestCase):
    def setUp(self):
        # Assuming these are example valid and invalid credentials
        self.valid_email = 'valid@example.com'
        self.valid_password = 'valid_password'
        self.invalid_password = 'invalid_password'

    def test_login_with_valid_candidate_credentials(self):
        response = self.client.post(
            reverse('login'),
            {'username': self.valid_email, 'password': self.valid_password}
        )

        # Assert successful login based on your redirect logic (replace as needed)
        self.assertRedirects(response, reverse('success_url'))

    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            reverse('login'),
            {'username': self.valid_email, 'password': self.invalid_password}
        )

        self.assertContains(response, 'Invalid email or password.')
        self.assertEqual(response.status_code, 200)  # Assert expected error code

    def test_login_with_valid_candidate_credentials_redirects(self):
        response = self.client.post(
            reverse('login'),
            {'username': self.valid_email, 'password': self.valid_password}
        )

        # Assert successful login based on your redirect logic (replace as needed)
        self.assertRedirects(response, reverse('success_url'))
