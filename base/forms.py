# forms.py

from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User

class ProfileUpdateForm(UserChangeForm):
    password = forms.CharField(label="New Password", strip=False, widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(label="Confirm New Password", strip=False, widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password
