from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse
from .views import create_post
from .models import Post2

#implement by Ron Cohen
class CreatePostTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_create_new_post_redirect(self):
        request = self.factory.post(reverse('create_post'),
                                    {'title': 'New Title', 'user_name': 'User123', 'content': 'New content'})
        response = create_post(request)

        self.assertRedirects(response, '/post_success/')  # Adjust redirect URL if necessary

    def test_create_new_post_database(self):
        Post2.objects.all().delete()  # Clear all existing posts
        request = self.factory.post(reverse('create_post'),
                                    {'title': 'New Title', 'user_name': 'User123', 'content': 'New content'})
        create_post(request)

        new_post = Post2.objects.get(title='New Title', user_name='User123', content='New content')
        self.assertIsNotNone(new_post)

    def test_render_all_posts(self):
        Post2.objects.create(title='Test Post', user_name='TestUser', content='Test content')
        request = self.factory.get(reverse('create_post'))
        response = create_post(request)

        self.assertEqual(response.status_code, 200)  # Assuming 200 for successful rendering
        self.assertTemplateUsed(response, 'after_login_forum.html')
        self.assertQuerysetEqual(response.context['posts'], Post2.objects.all(), transform=lambda x: x)

