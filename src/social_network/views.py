from django.shortcuts import render


def home_page(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'main/home.html', context)
