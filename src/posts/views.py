from django.shortcuts import render, redirect
from .models import *
from profiles.models import Profile
from .forms import *
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def all_posts_view(request):
    logged_in_user_profile = Profile.objects.get(user=request.user)

    user_profiles = list(logged_in_user_profile.get_friends())
    user_profiles.append(logged_in_user_profile.user)
    posts_qs = [post for post in Post.objects.all() if post.author.user in user_profiles]

    # Form for creating new post by the logged in user.
    new_post_form = PostModelForm()

    # Form for creating new comments on the posts by the logged in user.
    new_comment_form = CommentModelForm()

    context = {
        'posts_qs': posts_qs,
        'profile': logged_in_user_profile,
        'new_post_form': new_post_form,
        'new_comment_form': new_comment_form,
    }
    return render(request, 'posts/main.html', context)


@login_required
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

        data = {
            'value': like_obj.like_unlike_value,
            'likes': post.liked_by.all().count()
        }

        return JsonResponse(data, safe=False)
        # return redirect('main-posts-view')

    return redirect('main-posts-view')


@login_required
def submit_new_comment(request):

    if request.method == 'POST':
        logged_in_user_profile = Profile.objects.get(user=request.user)

        # Handle Comment form submission.
        new_comment_form = CommentModelForm(request.POST)
        if new_comment_form.is_valid():
            instance = new_comment_form.save(commit=False)
            instance.user = logged_in_user_profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()

    return redirect('main-posts-view')


@login_required
def create_post(request):

    if request.method == 'POST':
        logged_in_user_profile = Profile.objects.get(user=request.user)

        # Handle Post form submission.
        new_post_form = PostModelForm(request.POST, request.FILES)
        if new_post_form.is_valid():
            # Before saving the new post, we want to assign its author as the current logged in user.
            # Thus, to prevent automatic save, we pass the parameter commit=False as follows.
            instance = new_post_form.save(commit=False)
            instance.author = logged_in_user_profile
            instance.save()

    return redirect('main-posts-view')


# We use generic views so that the post cannot be deleted/updated directly using the url.
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('main-posts-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You are not authorized to delete this post.')
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'posts/update.html'
    success_url = reverse_lazy('main-posts-view')

    def form_valid(self, form):
        logged_in_user_profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == logged_in_user_profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You are not authorized to update this post.')
            return super().form_invalid(form)
