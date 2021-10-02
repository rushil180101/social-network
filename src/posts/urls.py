from django.urls import path
from .views import *

urlpatterns = [
    path('', all_posts_view, name='main-posts-view'),
    path('like-unlike-post', like_unlike_post, name='like-unlike-post'),
]
