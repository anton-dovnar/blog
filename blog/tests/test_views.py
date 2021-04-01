from django.test import TestCase, tag
from django.urls import reverse
from django.core.paginator import Paginator

from ..views import PostList, PostDetail
from .mixins import SetUpMixin


@tag('blog-views')
class ViewsTest(SetUpMixin, TestCase):

    def test_post_list_get(self):
        """
        - url namespace - ('blog:post-list')
        - request METHOD - GET
        - view - PostList
        """

        response = self.client.get(reverse('blog:post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, PostList.as_view().__name__)
        self.assertIn('post_list', response.context)
        self.assertIn('paginator', response.context)
        self.assertIsInstance(response.context.get('paginator'), Paginator)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_detail_get(self):
        """
        - url namespace - ('blog:post-detail')
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
