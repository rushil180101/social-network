from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import Profile


@login_required
def my_profile(request):
    logged_in_user_profile = Profile.objects.get(user=request.user)

    # We can populate a form in a GET request with existing values using the following parameters.
    # request.POST or None, request.FILES or None, instance=model_instance
    profile_update_form = ProfileUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=logged_in_user_profile
    )

    if request.method == 'POST':
        if profile_update_form.is_valid():
            profile_update_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('my-profile')

    context = {
        'profile': logged_in_user_profile,
        'profile_update_form': profile_update_form,
    }
    return render(request, 'profiles/myprofile.html', context)


@login_required
def received_invitations_view(request):
    logged_in_user_profile = Profile.objects.get(user=request.user)
    received_invitations_qs = Relationship.objects.invitations_received(logged_in_user_profile)
    senders = [invitation.sender for invitation in list(received_invitations_qs)]
    context = {
        'senders': senders,
    }
    return render(request, 'profiles/received_invites.html', context)


@login_required
def friends_list(request):
    logged_in_user_profile = Profile.objects.get(user=request.user)
    friends_profiles = [Profile.objects.get(user=i) for i in list(logged_in_user_profile.friends.all())]
    context = {
        'friends_profiles': friends_profiles,
    }
    return render(request, 'profiles/friends_list.html', context)


@login_required
def pending_requests(request):
    logged_in_user_profile = Profile.objects.get(user=request.user)
    sent_invitation_requests = Relationship.objects.invitations_sent(logged_in_user_profile)
    profiles = [invitation_request.receiver for invitation_request in sent_invitation_requests]
    context = {
        'profiles': profiles,
    }
    return render(request, 'profiles/pending_requests.html', context)


@login_required
def available_profiles_to_invite(request):
    available_profiles = Profile.objects.profiles_available_to_invite(request.user)
    context = {
        'available_profiles': available_profiles,
    }
    return render(request, 'profiles/available_profiles_to_invite.html', context)


@login_required
def send_friend_request(request):
    if request.method == 'POST':
        logged_in_user_profile = Profile.objects.get(user=request.user)
        sender = logged_in_user_profile
        receiver = Profile.objects.get(pk=request.POST.get('profile_pk'))
        Relationship.objects.create(
            sender=sender,
            receiver=receiver,
            status='sent'
        )
        messages.success(request, 'Friend Request has been sent.')
        return redirect('available-profiles-to-invite')
    return redirect('available-profiles-to-invite')


@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        logged_in_user_profile = Profile.objects.get(user=request.user)
        sender = logged_in_user_profile
        receiver = Profile.objects.get(pk=request.POST.get('profile_pk'))
        relationship = Relationship.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) |
            (Q(sender=receiver) & Q(receiver=sender))
        )
        if relationship:
            relationship.delete()

        logged_in_user_profile.friends.remove(receiver.user)
        receiver.friends.remove(logged_in_user_profile.user)
        logged_in_user_profile.save()
        receiver.save()

        messages.success(request, 'Removed from friends.')
        return redirect('my-friends-list')
    return redirect('my-friends-list')


@login_required
def accept_request(request):
    if request.method == 'POST':
        logged_in_user_profile = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=request.POST.get("profile_pk"))
        receiver = logged_in_user_profile
        sender.friends.add(receiver.user)
        receiver.friends.add(sender.user)
        relationship = Relationship.objects.get(sender=sender, receiver=receiver)
        relationship.delete()
        return redirect('my-received-invites')
    return redirect('my-received-invites')


@login_required
def reject_request(request):
    if request.method == 'POST':
        logged_in_user_profile = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=request.POST.get("profile_pk"))
        receiver = logged_in_user_profile
        relationship = Relationship.objects.get(sender=sender, receiver=receiver)
        relationship.delete()
        return redirect('my-received-invites')
    return redirect('my-received-invites')


@login_required
def delete_request(request):
    if request.method == 'POST':
        logged_in_user_profile = Profile.objects.get(user=request.user)
        sender = logged_in_user_profile
        receiver = Profile.objects.get(pk=request.POST.get("profile_pk"))
        relationship = Relationship.objects.get(sender=sender, receiver=receiver)
        relationship.delete()
        return redirect('pending-requests')
    return redirect('pending-requests')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["posts"] = self.get_object().get_posts()
        context["len_posts"] = self.get_object().get_posts_count()
        context["friends_count"] = self.get_object().get_friends_count()
        logged_in_user_profile = Profile.objects.get(user=self.request.user)

        # Check if the profile is connected as a friend with current logged in user.
        condition_1 = self.request.user in list(self.get_object().friends.all())
        condition_2 = self.get_object().user in list(logged_in_user_profile.friends.all())
        if condition_1 and condition_2:
            context["is_friends"] = True
        else:
            context["is_friends"] = False

        # Check for received friend request.
        try:
            relationship = Relationship.objects.get(sender=self.get_object(), receiver=logged_in_user_profile)
        except Relationship.DoesNotExist:
            relationship = None
        context["received_request"] = True if relationship is not None else False

        # Check for pending sent request.
        try:
            relationship = Relationship.objects.get(sender=logged_in_user_profile, receiver=self.get_object())
        except Relationship.DoesNotExist:
            relationship = None
        context["pending_sent_request"] = True if relationship is not None else False

        return context
