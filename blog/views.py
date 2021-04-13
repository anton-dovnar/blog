from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_GET
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm, SearchForm
from .models import Post


class PostList(generic.ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 8
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_slug = self.kwargs.get('tag_slug', None)

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])

        return queryset.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.kwargs.get('tag_slug', None)
        if tag:
            context['tag'] = tag
        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Infinite scroll with ajax request.
        """

        if self.request.is_ajax():
            return render(self.request, 'blog/post_list_ajax.html', context)
        return super().render_to_response(context, **response_kwargs)


class PostDetail(generic.edit.FormMixin, generic.DetailView):
    model = Post
    form_class = CommentForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        comments = post.comments.filter(active=True)
        post_tags_pks = post.tags.values_list('pk', flat=True)
        similar_posts = Post.objects.filter(status='published', tags__in=post_tags_pks).exclude(pk=post.pk)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-published')
        context['similar_posts'] = similar_posts
        context['comments'] = comments
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = self.get_object()
        new_comment = form.save(commit=False)
        new_comment.post = self.object
        new_comment.save()
        return self.render_to_response(self.get_context_data(post=self.object))

    def render_to_response(self, context, **response_kwargs):
        form = self.get_form()
        if self.request.is_ajax() and form.is_valid():
            return render(self.request, 'blog/post_comments.html', context)
        return super().render_to_response(context, **response_kwargs)


@method_decorator(sensitive_post_parameters(), name='post')
class PostShare(SuccessMessageMixin, generic.FormView):
    form_class = EmailPostForm
    template_name = 'blog/post_share.html'
    success_url = reverse_lazy('blog:post-list')
    success_message = 'Mail sent successfully'

    def form_valid(self, form):
        post = get_object_or_404(
            Post,
            slug=self.kwargs['post'],
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day']
        )
        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        form.send(post, post_url)
        return super().form_valid(form)


@require_GET
def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.objects.filter(status='published') \
                                  .annotate(rank=SearchRank(search_vector, search_query)) \
                                  .filter(rank__gte=0.3).order_by('-rank')
            return render(request, 'blog/search.html', {'query': query, 'results': results})

    return redirect('blog:post-list')
