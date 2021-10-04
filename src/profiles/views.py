from django.shortcuts import render, redirect
from .forms import *
from .models import Profile


def my_profile(request):
    logged_in_user_profile = Profile.objects.get(user=request.user)

    # We can populate a form in a GET request with existing values using the following parameters.
    # request.POST or None, request.FILES or None, instance=model_instance
    profile_update_form = ProfileUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=logged_in_user_profile
    )
    profile_updated = False

    if request.method == 'POST':
        if profile_update_form.is_valid():
            profile_update_form.save()
            profile_updated = True

    context = {
        'profile': logged_in_user_profile,
        'profile_update_form': profile_update_form,
        'profile_updated': profile_updated,
    }
    return render(request, 'profiles/myprofile.html', context)


def received_invitations_view(request):
    logged_in_user_profile = Profile.objects.get(user=request.user)
    received_invitations_qs = Relationship.objects.invitations_received(logged_in_user_profile)

    context = {
        'received_invitations_qs': received_invitations_qs,
    }

    return render(request, 'profiles/received_invites.html', context)
