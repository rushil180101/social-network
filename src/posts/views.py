from django.shortcuts import render, redirect
from .models import *
from profiles.models import Profile


def all_posts_view(request):
    posts_qs = Post.objects.all()
    logged_in_user_profile = Profile.objects.get(user=request.user)

    context = {
        'posts_qs': posts_qs,
        'profile': logged_in_user_profile,
    }
    return render(request, 'posts/main.html', context)
# Note: The above function all_posts_view() can also be implemented with Django ListView


def like_unlike_post(request):

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        cb_profile = Profile.objects.get(user=request.user)
        # cb_profile ==> clicked by profile, i.e., the profile of the current logged in user
        # who clicks on the like/unlike button.

        if cb_profile in post.liked_by.all():
            post.liked_by.remove(cb_profile)
        else:
            post.liked_by.add(cb_profile)

        # Handle Like model's instance
        like_obj, created = Like.objects.get_or_create(user=cb_profile, post=post)

        if created:
            like_obj.like_unlike_value = 'Like'
        else:
            if like_obj.like_unlike_value == 'Like':
                like_obj.like_unlike_value = 'Unlike'
            else:
                like_obj.like_unlike_value = 'Like'

        like_obj.save()
        post.save()
        return redirect('main-posts-view')

    return redirect('main-posts-view')
