from model_mommy import mommy

from ..models import Post


class SetUpMixin:
    """
    Setup data for testing.
    """

    def setUp(self):
        self.post = mommy.make(Post)
