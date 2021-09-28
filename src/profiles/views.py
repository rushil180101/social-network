from django.shortcuts import render
from .models import Profile


def my_profile(request):
    user_profile_obj = Profile.objects.get(user=request.user)
    context = {
        'profile': user_profile_obj,
    }
    return render(request, 'profiles/myprofile.html', context)
