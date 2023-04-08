from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, 'Account/signup.html', {'form' : form})

def login_views(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, 'Invalid username/password combination.')
    else:
        form = LoginForm()
    return render(request, 'Account/login.html', {'form' : form})