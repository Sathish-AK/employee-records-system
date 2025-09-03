from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ChangePasswordForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']  # ✅ use password1
            )
            messages.success(request, "🎉 Registration successful. Please log in.")
            return redirect('login')
        else:
            print("inside error")
            # messages.error(request, "⚠ Please correct the errors below.")
            print(form.errors)  # Debug in console
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home')
            messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == "POST":
        profile = request.user.profile
        profile.full_name = request.POST.get("full_name","")
        profile.bio = request.POST.get("bio","")
        profile.save()
        messages.success(request, "Profile updated")
    return render(request, "accounts/profile.html")

@login_required
def change_password_view(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if request.user.check_password(form.cleaned_data['old_password']):
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                messages.success(request, "Password changed. Please log in again.")
                logout(request)
                return redirect('login')
            messages.error(request, "Old password incorrect")
    else:
        form = ChangePasswordForm()
    return render(request, "accounts/change_password.html", {"form": form})
