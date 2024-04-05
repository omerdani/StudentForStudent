import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'StudentForStudent.settings'  # replace with your actual settings module

import django
django.setup()

import unittest
from django.test import RequestFactory
from S4S.models import Candidate, Student, Graduate, Post2, Blog
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


class TestViews(unittest.TestCase):


    def setUp(self):
        super().setUp()

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
        def test_login(self):
            candidate = None
            try:
                candidate = Candidate.objects.create(**self.user_data2)

                client = Client()

                login_data = {
                    'email': self.user_data2['email'],
                    'password': self.user_data2['password']
                }

                response = client.post('/login/', data=login_data)
                self.assertEqual(response.status_code, 302)  # Check if the request was successful

                self.assertEqual(client.session['email'], self.user_data2['email'])  # Check if the user is logged in

            finally:
                if candidate is not None:
                    candidate.delete()












