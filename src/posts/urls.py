from django.urls import path
from .views import all_posts_view

urlpatterns = [
    path('', all_posts_view, name='main-post-view'),
]
