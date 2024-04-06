import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'StudentForStudent.settings'  # replace with your actual settings module

import django
django.setup()

import unittest
from django.test import RequestFactory
from S4S.models import Candidate, Student, Graduate, Post2, Blog, Admin, Comment
from S4S.blogim import create_post
from S4S.views import signup, login
from S4S.superusers import delete_post_Admin
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from unittest.mock import patch
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.sessions.middleware import SessionMiddleware
from S4S.views import signup, login, logout, home
from S4S.models import Candidate, Student, Graduate, Post2, Blog, Admin
from S4S.likes import like_post
from S4S.my_email import send_test_email, enter_code



class TestViews(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.client = Client()  # Add this line
        self.factory = RequestFactory()
        self.user_data = {
            'status': 'Candidate',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'password',
            'name': 'John',
        }
        self.user_data2 = {
            'first_name': 'John',
            'last_name': 'DUDU',
            'email': 'johndudu@gmail.com',
            'password': '656565'
        }

        self.test_data = {
            'title': 'Test Post Title',
            'user_name': 'Test User',
            'content': 'This is a test post content.',
            'blog': 'Test Blog',
        }


    def test_signup(self):
        request = self.factory.post('/signup/', data=self.user_data)
        response = signup(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Candidate.objects.filter(email=self.user_data['email']).exists())
        Candidate.objects.last().delete()

    def test_create_post(self):
        candidate = None
        blog1 = None
        try:
            candidate = Candidate.objects.create(**self.user_data2)
            blog1 = Blog.objects.create(title='Test Blog', description='Test Blog Description')

            client = Client()
            session = client.session
            session['status'] = 'Candidate'
            session['email'] = candidate.email
            session['first_name'] = candidate.first_name
            session['last_name'] = candidate.last_name
            session.save()
            print(client.session.get('email'))

        finally:
            if candidate is not None:
                candidate.delete()
            if blog1 is not None:
                blog1.delete()

    def test_edit_post(self):
        candidate = None
        blog1 = None
        post1 = None
        try:
            candidate = Candidate.objects.create(**self.user_data2)
            blog1 = Blog.objects.create(title='Test Blog', description='Test Blog Description')
            post1 = Post2.objects.create(title='Original Title', content='Original Content',
                                         user_name=candidate.first_name + ' ' + candidate.last_name, blog=blog1,
                                         user_email=candidate.email)

            client = Client()
            session = client.session
            session['status'] = 'Candidate'
            session['email'] = candidate.email
            session['first_name'] = candidate.first_name
            session['last_name'] = candidate.last_name
            session.save()

            new_post_data = {
                'title': 'Updated Title',
                'content': 'Updated Content'
            }

            response = client.post(f'/edit_post/{post1.id}/', data=new_post_data)
            self.assertEqual(response.status_code, 302)  # Check if the request was successful

            post1.refresh_from_db()  # Refresh the post data from the database
            self.assertEqual(post1.title, new_post_data['title'])  # Check if the title was updated
            self.assertEqual(post1.content, new_post_data['content'])  # Check if the content was updated

        finally:
            if candidate is not None:
                candidate.delete()
            if blog1 is not None:
                blog1.delete()
            if post1 is not None:
                post1.delete()

    def test_login(self):

        candidate = None
        try:
            candidate = Candidate.objects.create(**self.user_data2)

            client = Client()

            login_data = {
                'email': self.user_data2['email'],
                'password': self.user_data2['password']
            }

            session = client.session
            session['status'] = 'Candidate'
            session['email'] = candidate.email
            session.save()

            response = client.post('/login/', data=login_data)
            self.assertEqual(response.status_code, 200)  # Check if the request was successful

            self.assertEqual(client.session['email'], self.user_data2['email'])  # Check if the user is logged in

        finally:
            if candidate is not None:
                candidate.delete()



    def test_like_post(self):
        candidate = None
        blog1 = None
        post1 = None
        try:
            candidate = Candidate.objects.create(**self.user_data2)
            blog1 = Blog.objects.create(title='Test Blog', description='Test Blog Description')
            post1 = Post2.objects.create(title='Original Title', content='Original Content',
                                         user_name=candidate.first_name + ' ' + candidate.last_name, blog=blog1,
                                         user_email=candidate.email)

            client = Client()
            session = client.session
            session['status'] = 'Candidate'
            session['email'] = candidate.email
            session['first_name'] = candidate.first_name
            session['last_name'] = candidate.last_name
            session.save()

            initial_likes_count = post1.likes_count

            factory = RequestFactory()
            request = factory.get('/')
            request.session = session

            response = like_post(request, post1.id)
            self.assertEqual(response.status_code, 302)  # Check if the request was successful

            post1.refresh_from_db()  # Refresh the post data from the database
            print(post1.likes_count)
            self.assertEqual(post1.likes_count, initial_likes_count + 1)  # Check if the likes count was incremented

        finally:
            if candidate is not None:
                candidate.delete()
            if blog1 is not None:
                blog1.delete()
            if post1 is not None:
                post1.delete()
    def test_delete_post(self):
        candidate = None
        blog1 = None
        post1 = None
        try:
            # Create necessary objects
            candidate = Candidate.objects.create(**self.user_data2)
            blog1 = Blog.objects.create(title='Test Blog', description='Test Blog Description')
            post1 = Post2.objects.create(title='Original Title', content='Original Content',
                                         user_name=candidate.first_name + ' ' + candidate.last_name, blog=blog1,
                                         user_email=candidate.email)
            # Create a User instance for the candidate
            user = User.objects.create_user(username=candidate.email, password=self.user_data2['password'])
            # Associate the User instance with the Candidate instance
            candidate.user = user
            candidate.save()
            # Log the user in using the Client instance
            client = Client()
            client.login(username=candidate.email, password=self.user_data2['password'])
            # Check the initial count of Post2 objects
            initial_post_count = Post2.objects.count()
            # Check if the Post2 object exists
            if Post2.objects.filter(id=post1.id).exists():
                # Send a DELETE request to the delete_post_Admin view
                response = client.post(reverse('delete_post', args=[post1.id]))
                # Check if the request was successful
                self.assertEqual(response.status_code, 302)
                # Check if the count of Post2 objects has decreased
                self.assertEqual(Post2.objects.count(), initial_post_count - 1)
            else:
                self.fail('Post2 object does not exist')
        finally:
            # Clean up
            if candidate is not None:
                candidate.delete()
            if blog1 is not None:
                blog1.delete()
            if post1 is not None and Post2.objects.filter(id=post1.id).exists():
                post1.delete()
            if user is not None:
                user.delete()

    def test_my_profile_redirect(self):
        response = self.client.get(reverse('My_Profile'))
        self.assertEqual(response.status_code, 200)


    def test_logout_redirect(self):
       response = self.client.get(reverse('logout'))
       self.assertEqual(response.status_code, 302)
    def test_data_redirect(self):
        response = self.client.get(reverse('data'))
        self.assertEqual(response.status_code, 200)

    def test_forgotpass_redirect(self):
        response = self.client.get(reverse('forgotpass'))
        self.assertEqual(response.status_code, 200)

    def test_mainforum_redirect(self):
        response = self.client.get(reverse('mainforum'))
        self.assertEqual(response.status_code, 200)

    def test_active_sessions_redirect(self):
        response = self.client.get(reverse('active_sessions'))
        self.assertEqual(response.status_code, 200)

    def test_enter_code_redirect(self):
        response = self.client.get(reverse('enter_code'))
        self.assertEqual(response.status_code, 200)
    def test_superuser_home_redirect(self):
        response = self.client.get(reverse('superuser_home'))
        self.assertEqual(response.status_code, 302)
    def test_manage_users_redirect(self):
        response = self.client.get(reverse('manage_users'))
        self.assertEqual(response.status_code, 200)

    def test_comment_post(self):
        candidate = None
        blog1 = None
        post1 = None
        try:
            # Create necessary objects
            candidate = Candidate.objects.create(**self.user_data2)
            blog1 = Blog.objects.create(title='Test Blog', description='Test Blog Description')
            post1 = Post2.objects.create(title='Original Title', content='Original Content',
                                         user_name=candidate.first_name + ' ' + candidate.last_name, blog=blog1,
                                         user_email=candidate.email)
            # Log the user in using the Client instance
            client = Client()
            client.login(username=candidate.email, password=self.user_data2['password'])
            # Check the initial count of Comment objects
            initial_comment_count = Comment.objects.count()
            # Create comment data
            comment_data = {
                'content': 'This is a test comment',
                'post': post1.id
            }
            # Send a POST request to the post_detail view with the comment data
            response = client.post(reverse('post_detail', args=[post1.id]), data=comment_data)
            # Check if the request was successful
            self.assertEqual(response.status_code, 302)
            # Check if the comment was added to the post
            self.assertEqual(Comment.objects.count(), initial_comment_count + 1)
        finally:
            # Clean up
            if candidate is not None:
                candidate.delete()
            if blog1 is not None:
                blog1.delete()
            if post1 is not None and Post2.objects.filter(id=post1.id).exists():
                post1.delete()