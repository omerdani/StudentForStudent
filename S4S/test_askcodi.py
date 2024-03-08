from django.test import TestCase
from django.test import RequestFactory
from S4S.models import Post2
from S4S.views import delete_post_Admin

class DeletePostAdminTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_post_exists(self):
        post = Post2.objects.create(title='Test Post', content='Test Content', user_name='test_user')
        self.assertTrue(Post2.objects.filter(pk=post.id).exists())

    def test_post_deleted(self):
        post = Post2.objects.create(title='Test Post', content='Test Content', user_name='test_user')
        post_id = post.id

        # Delete the post
        post.delete()

        self.assertFalse(Post2.objects.filter(pk=post_id).exists())

    def test_redirect_url(self):
        post = Post2.objects.create(title='Test Post', content='Test Content', user_name='test_user')
        request = self.factory.post('/delete_post/', data={'post_id': post.id})
        response = delete_post_Admin(request, post_id=post.id)

        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'expected_redirect_url')
