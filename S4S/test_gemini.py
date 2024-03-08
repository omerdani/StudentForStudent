from django.test import RequestFactory
from django.contrib.auth.models import User
import unittest
from .models import Candidate, Student, Graduate, Post2
from .views import signup, display_data, login, create_post, delete_post_Admin
from django.test import TestCase, Client
from django.urls import reverse  # Import for URL resolution
# added by yarin ivgy
class SignupTest(TestCase):
    def test_existing_email(self):
        # Create existing users (Candidate and Student)
        candidate = Candidate.objects.create(email='test@example.com')
        Student.objects.create(email='test@example.com')

        # Prepare POST data
        data = {
            'status': 'Candidate',  # Doesn't matter which status, both models are checked
            'name': 'John',
            'lastName': 'Doe',
            'email': 'test@example.com',
            'password': 'secret123',
        }

        # Send POST request
        client = Client()
        response = client.post(reverse('signup'), data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'SignUp.html')
        self.assertContains(response, 'User with this email already exists.')

        def test_successful_signup_candidate(self):
            data = {
                'status': 'Candidate',
                'name': 'Jane',
                'lastName': 'Smith',
                'email': 'jane.smith@example.com',
                'password': 'securepassword',
            }

            client = Client()
            response = client.post(reverse('signup'), data)

            self.assertEqual(response.status_code, 302)  # Redirect (302 status code)
            self.assertRedirects(response, reverse('login'))  # Redirect to Login.html

        def test_object_creation_student(self):
            data = {
                'status': 'Student',
                'name': 'Mike',
                'lastName': 'Lee',
                'email': 'mike.lee@example.com',
                'password': 'strongpass',
                'year': 2024,  # Assuming year is required for Student model
            }

            client = Client()
            client.post(reverse('signup'), data)

            # Check if Student object is created
            student = Student.objects.get(email=data['email'])
            self.assertEqual(student.first_name, data['name'])
            self.assertEqual(student.last_name, data['lastName'])
            self.assertEqual(student.select_year, data['year'])  # Assuming year is a field