from django.core.paginator import Paginator
from django.test import TestCase, override_settings, tag
from django.urls import reverse

from ..forms import EmailPostForm
from ..views import PostDetail, PostList, PostShare
from .mixins import SetUpMixin


@tag('blog-views')
class ViewsTest(SetUpMixin, TestCase):

    def test_post_list_get(self):
        """
        - reverse - ('blog:post-list')
        - request METHOD - GET
        - view - PostList
        """

        response = self.client.get(reverse('blog:post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, PostList.as_view().__name__)
        self.assertIn('posts', response.context)
        self.assertIn('paginator', response.context)
        self.assertIsInstance(response.context.get('paginator'), Paginator)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_list_by_tag_get(self):
        """
        - reverse - ('blog:post-list-by-tag')
        - request METHOD - GET
        - view - PostList
        """

        self.post.tags.add('django')
        self.post.save()
        response = self.client.get(reverse('blog:post-list-by-tag', args=['django']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, PostList.as_view().__name__)

    def test_post_detail_get(self):
        """
        - reverse - ('blog:post-detail')
        - request METHOD - GET
        - view - PostDetail
        """

        self.post.status = 'published'
        self.post.save()
        url = self.post.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, PostDetail.as_view().__name__)
        self.assertIn('post', response.context)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_detail_comment_post(self):
        """
        - reverse - ('blog:post-detail')
        - request METHOD - GET
        - view - PostDetail
        """

        self.post.status = 'published'
        self.post.save()
        url = self.post.get_absolute_url()
        data = {
            'name': 'Ivan',
            'email': 'ivan@gmail.com',
            'body': 'This is my first comment!'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, PostDetail.as_view().__name__)

    def test_post_share_get(self):
        """
        - reverse - ('blog:post-share')
        - request METHOD - GET
        - view - PostShare
        """

        self.post.status = 'published'
        self.post.save()
        response = self.client.get(reverse('blog:post-share', args=[
            self.post.published.year, self.post.published.month, self.post.published.day, self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, PostShare.as_view().__name__)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context.get('form'), EmailPostForm)
        self.assertTemplateUsed(response, 'blog/post_share.html')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend')
    def test_post_share_post(self):
        """
        - reverse - ('blog:post-share')
        - request METHOD - POST
        - view - Post Share
        """

        self.post.status = 'published'
        self.post.save()
        data = {
            'name': 'Ivan',
            'email': 'ivan@gmail.com',
            'to': 'vasily@gmail.com',
            'comments': 'Hello, interesting content!',
        }
        response = self.client.post(reverse('blog:post-share', args=[
            self.post.published.year, self.post.published.month, self.post.published.day, self.post.slug]), data=data)
        self.assertRedirects(response, reverse('blog:post-list'))
