from django.urls import path

from . import views
from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post-list'),
    path('tag/<slug:tag_slug>/', views.PostList.as_view(), name='post-list-by-tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.PostDetail.as_view(), name='post-detail'),
    path('<int:post_pk>/share/', views.PostShare.as_view(), name='post-share'),
    path('search/', views.post_search, name='post-search'),
    path('feed/', LatestPostFeed(), name='post-feed'),
]
