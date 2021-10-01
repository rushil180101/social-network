from django.shortcuts import render
from .models import *


def all_posts_view(request):
    posts_qs = Post.objects.all()

    context = {
        'posts_qs': posts_qs,
    }
    return render(request, 'posts/main.html', context)
