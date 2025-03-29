from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from .models import *

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
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created! Please wait for admin approval.")
            return redirect("signin")  # Redirect to login page
    else:
        form = SignUpForm()
    
    return render(request, "signup.html", {"form": form})

def profile(request):
    return render(request, 'profile.html', {})

def dashboard(request):
    return render(request, 'dashboard.html', {})

def approve(request):
    accounts = Profile.objects.filter(is_approved=False)  # Get only unapproved users
    context = {
        'accounts': accounts,
    }
    return render(request, 'approve.html', context)

def approve_user(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.is_approved = True
    profile.save()
    messages.success(request, f"{profile.user.username} has been approved!")
    return redirect('approve')

def reject_user(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.user.delete()  # Deletes the user and profile
    messages.error(request, f"User {profile.user.username} has been declined.")
    return redirect('approve')