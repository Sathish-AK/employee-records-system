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
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        # ✅ Check old password
        if not request.user.check_password(old_password):
            messages.error(request, "❌ Old password is incorrect.")
            return redirect("change_password")

        # ✅ Prevent same old and new password
        if old_password == new_password1:
            messages.error(request, "⚠ New password cannot be the same as the old password.")
            return redirect("change_password")

        # ✅ Check match
        if new_password1 != new_password2:
            messages.error(request, "❌ New password and Confirm Password do not match.")
            return redirect("change_password")

        # ✅ Strong password check
        if len(new_password1) < 8:
            messages.error(request, "⚠ Password must be at least 8 characters long.")
            return redirect("change_password")
        if not re.search(r"[A-Z]", new_password1):
            messages.error(request, "⚠ Password must contain at least one uppercase letter.")
            return redirect("change_password")
        if not re.search(r"[a-z]", new_password1):
            messages.error(request, "⚠ Password must contain at least one lowercase letter.")
            return redirect("change_password")
        if not re.search(r"[0-9]", new_password1):
            messages.error(request, "⚠ Password must contain at least one number.")
            return redirect("change_password")
        if not re.search(r"[@$!%*?&]", new_password1):
            messages.error(request, "⚠ Password must contain at least one special character (@$!%*?&).")
            return redirect("change_password")

        # ✅ All checks passed → set new password
        request.user.set_password(new_password1)
        request.user.save()
        messages.success(request, "✅ Password changed successfully. Please log in again.")
        return redirect("login")

    return render(request, "accounts/change_password.html")
