from django.test import TestCase, tag
from django.utils.text import slugify
from model_mommy import mommy

from blog.models import Post


@tag('blog-models')
class ModelsTest(TestCase):

    def setUp(self):
        self.post = mommy.make(Post)

    def test_post_creation(self):
        self.assertIsInstance(self.post, Post)
        self.assertEqual(self.post.__str__(), self.post.title)
        self.assertEqual(self.post.slug, slugify(self.post.title))
