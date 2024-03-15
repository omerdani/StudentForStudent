from django.test import RequestFactory
from django.contrib.auth.models import User
import unittest
from .models import Candidate, Student, Graduate, Post2
from .views import signup, login, create_post, delete_post_Admin
from django.test import TestCase, Client
from django.urls import reverse  # Import for URL resolution

class TestViews(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_data = {
            'status': 'Candidate',
            'name': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'password',
            'year': '2023',
            'workplace': 'Company XYZ'
        }


        self.test_data = {
            'title': 'Test Post Title',
            'user_name': 'Test User',
            'content': 'This is a test post content.','id':337
            }

#written by yarin evgy
    def test_signup(self):
        request = self.factory.post('/signup/', data=self.user_data)
        response = signup(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Candidate.objects.filter(email=self.user_data['email']).exists())

#written by israel yaakubov

    def test_login(self):
        candidate = Candidate.objects.create(email='test@example.com', password='password')
        request = self.factory.post('/login/', data={'username': candidate.email, 'password': 'password'})
        response = login(request)
        self.assertEqual(response.status_code, 302)

#written by ron cohen

    def test_create_post(self):
        initial_post_count = Post2.objects.count()

        Post2.objects.create(**self.test_data)

        new_post_count = Post2.objects.count()

        self.assertEqual(new_post_count, initial_post_count + 1)

        created_post = Post2.objects.last()
        self.assertEqual(created_post.title, self.test_data['title'])
        self.assertEqual(created_post.content, self.test_data['content'])
        self.assertEqual(created_post.user_name, self.test_data['user_name'])

        created_post.delete()

#written by omer daniel

    def test_delete_post_Admin(self):
        post = Post2.objects.create(title='Test Post', content='Test Content', user_name='test_user',id=1234)
        request = self.factory.post('/delete_post/', data={'post_id': post.id})
        response = delete_post_Admin(request, post_id=post.id)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post2.objects.filter(pk=post.id).exists())

