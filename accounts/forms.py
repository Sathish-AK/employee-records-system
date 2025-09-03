from django import forms
from django.contrib.auth.models import User
import re

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("⚠ Username already exists. Please choose another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("⚠ Email already registered. Try logging in instead.")
        return email

    def clean_password1(self):
        pw = self.cleaned_data.get("password1")
        if len(pw) < 8:
            raise forms.ValidationError("⚠ Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", pw):
            raise forms.ValidationError("⚠ Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", pw):
            raise forms.ValidationError("⚠ Password must contain at least one lowercase letter.")
        if not re.search(r"\d", pw):
            raise forms.ValidationError("⚠ Password must contain at least one number.")
        if not re.search(r"[@$!%*?&]", pw):
            raise forms.ValidationError("⚠ Password must contain at least one special character (@, $, !, %, *, ?, &).")
        return pw

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("password1")
        pw2 = cleaned_data.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("⚠ Passwords do not match.")
        return cleaned_data



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
