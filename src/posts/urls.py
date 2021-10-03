from django.urls import path
from .views import *

urlpatterns = [
    path('', all_posts_view, name='main-posts-view'),
    path('like-unlike-post', like_unlike_post, name='like-unlike-post'),
    path('submit-new-comment', submit_new_comment, name='submit-new-comment'),
    path('create-post', create_post, name='create-post'),
]
