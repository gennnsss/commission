from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def home(request):
    return render(request, 'index.html')

def signin(request):
    if request.user.is_authenticated:
        return render(request, "signin.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")  # Redirect to the same page after login
        else:
            return render(request, "signin.html", {"error": "Invalid username or password"})

    return render(request, "signin.html")

def signout(request):
    logout(request)
    return redirect("signin")

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            return render(request, "signup.html", {"error": "Passwords do not match"})
        
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect("signin")

    return render(request, "signup.html")

def profile(request):
    return render(request, 'profile.html', {})

def dashboard(request):
    return render(request, 'dashboard.html', {})

