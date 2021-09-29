from django.shortcuts import render, redirect
from .forms import *
from .models import Profile


def my_profile(request):
    user_profile_obj = Profile.objects.get(user=request.user)

    # We can populate a form in a GET request with existing values using the following parameters.
    # request.POST or None, request.FILES or None, instance=model_instance
    profile_update_form = ProfileUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=user_profile_obj
    )
    profile_updated = False

    if request.method == 'POST':
        if profile_update_form.is_valid():
            profile_update_form.save()
            profile_updated = True

    context = {
        'profile': user_profile_obj,
        'profile_update_form': profile_update_form,
        'profile_updated': profile_updated,
    }
    return render(request, 'profiles/myprofile.html', context)
