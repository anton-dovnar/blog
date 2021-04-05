from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()


class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique_for_date='published')
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-published',)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super().save(**kwargs)

    def get_absolute_url(self):
        return reverse(
            'blog:post-detail', args=[self.published.year, self.published.month, self.published.day, self.slug])


class Comment(models.Model):

    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    body = models.TextField()
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('created', )

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
