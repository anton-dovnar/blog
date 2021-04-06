from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import Comment, Post


class EmailPostForm(forms.Form):
    """
    Form for share posts via email.
    """

    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def send(self, post: Post, post_url: str) -> None:
        cd = self.cleaned_data
        subject = f"{cd['name']} recommends read {post.title}"
        message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s comments: {cd['comments']}"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']], fail_silently=True)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()
