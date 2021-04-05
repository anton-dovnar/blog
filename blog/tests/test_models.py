from django.test import TestCase, tag
from django.utils.text import slugify

from ..models import Comment, Post
from .mixins import SetUpMixin


@tag('blog-models')
class ModelsTest(SetUpMixin, TestCase):

    def test_post_creation(self):
        self.assertIsInstance(self.post, Post)
        self.assertEqual(self.post.__str__(), self.post.title)
        self.assertEqual(self.post.slug, slugify(self.post.title))

    def test_comment_creation(self):
        self.assertIsInstance(self.comment, Comment)
        self.assertEqual(self.comment.__str__(), f"Comment by {self.comment.name} on {self.comment.post}")
