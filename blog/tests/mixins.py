from model_mommy import mommy

from ..models import Post, Comment


class SetUpMixin:
    """
    Setup data for testing.
    """

    def setUp(self):
        self.post = mommy.make(Post)
        self.comment = mommy.make(Comment)
