from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import MedecinRegisterForm, MedecinLoginForm

from django.shortcuts import render, redirect
from .forms import MedecinRegisterForm

def register(request):
    if request.method == 'POST':
        form = MedecinRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # This will create the user
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = MedecinRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = MedecinLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')  # Redirect to the home page after login
    else:
        form = MedecinLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to home page after logout
