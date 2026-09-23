import re

from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from blog.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    password = forms.CharField(widget=forms.PasswordInput())

    # Field-level validation (runs before clean())
    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        errors = []
        # Keep these in sync with your model constraints
        if len(username) < 4:
            errors.append("Username must be at least 4 characters long.")
        if len(username) > 150:
            errors.append("Username cannot exceed 150 characters.")
        # Only letters/digits/underscore:
        if not re.fullmatch(r"\w+", username):
            errors.append("Username can only contain letters, digits, and underscores.")
        if errors:
            raise ValidationError(" ".join(errors))
        return username

    # Field-level validation (runs before clean())
    def clean_password(self):
        password = self.cleaned_data.get("password") or ""
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            errors.append("Password must contain at least one digit.")
        if not any(char.isupper() for char in password):
            errors.append("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            errors.append("Password must contain at least one lowercase letter.")
        if not any(char in "!@#$%^&" for char in password):
            errors.append("Password must contain at least one special character.")
        # TODO: check against common passwords list
        if errors:
            raise ValidationError(" ".join(errors))
        return password
    # Runs after all field-level validations have succeeded
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user