from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm


def home_page(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'main/home.html', context)


def sign_up_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile created successfully. Login with the credentials.')
            return redirect('login')

    context = {'form': form}
    return render(request, 'main/sign_up.html', context)


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('my-profile')
        else:
            messages.error(request, 'User does not exist.')

    return render(request, 'main/login_page.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('home-page')

