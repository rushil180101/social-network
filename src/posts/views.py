from django.shortcuts import render, redirect
from .models import *
from profiles.models import Profile
from .forms import *


def all_posts_view(request):
    posts_qs = Post.objects.all()
    logged_in_user_profile = Profile.objects.get(user=request.user)

    # Form for creating new post by the logged in user.
    new_post_form = PostModelForm()

    # Form for creating new comments on the posts by the logged in user.
    new_comment_form = CommentModelForm()

    if request.method == 'POST':
        # Handle Post form submission
        if 'submit_post_form' in request.POST:
            new_post_form = PostModelForm(request.POST, request.FILES)
            if new_post_form.is_valid():
                # Before saving the new post, we want to assign its author as the current logged in user.
                # Thus, to prevent automatic save, we pass the parameter commit=False as follows.
                instance = new_post_form.save(commit=False)
                instance.author = logged_in_user_profile
                instance.save()

                # Create new empty form once the old post form is submitted and saved.
                new_post_form = PostModelForm()

        # Handle Comment form submission
        if 'submit_comment_form' in request.POST:
            new_comment_form = CommentModelForm(request.POST)
            if new_comment_form.is_valid():
                instance = new_comment_form.save(commit=False)
                instance.user = logged_in_user_profile
                instance.post = Post.objects.get(id=request.POST.get('post_id'))
                instance.save()

                # Create new empty form once the old one is submitted.
                new_comment_form = CommentModelForm()

    context = {
        'posts_qs': posts_qs,
        'profile': logged_in_user_profile,
        'new_post_form': new_post_form,
        'new_comment_form': new_comment_form,
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
