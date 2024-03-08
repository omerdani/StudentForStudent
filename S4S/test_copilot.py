
from django.test import TestCase
from django.urls import reverse
# added by israel yakubov
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

        # Assert redirect to the appropriate URL upon successful login
        self.assertRedirects(response, '/success/')

    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            reverse('login'),
            {'username': self.valid_email, 'password': self.invalid_password}
        )

        # Assert that the error message matches the one returned by the view
        self.assertContains(response, 'Invalid email or password.')
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_candidate_credentials_redirects(self):
        response = self.client.post(
            reverse('login'),
            {'username': self.valid_email, 'password': self.valid_password}
        )

        # Assert redirect to the appropriate URL upon successful login
        self.assertRedirects(response, '/success/')