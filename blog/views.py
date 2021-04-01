from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Post


class PostList(generic.ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post_list.html'


class PostDetail(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'

    def get_object(self):
        post = get_object_or_404(
            Post,
            slug=self.kwargs['post'],
            status='published',
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day']
        )
        return post
