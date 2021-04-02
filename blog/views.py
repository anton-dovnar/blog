from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.debug import sensitive_post_parameters

from .forms import EmailPostForm
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


@method_decorator(sensitive_post_parameters(), name='post')
class PostShare(SuccessMessageMixin, generic.FormView):
    form_class = EmailPostForm
    template_name = 'blog/post_share.html'
    success_url = reverse_lazy('blog:post-list')
    success_message = 'Mail sent successfully'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        form.send(post, post_url)
        return super().form_valid(form)
