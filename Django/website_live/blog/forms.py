import re

from django import forms
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

from blog.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        # TODO: validation logic
        pass

    def clean_password(self):
        pwd = self.cleaned_data['password']
        errors = []

        if not any(c.isdigit() for c in pwd):
            errors.append('Password must contain at least one number')
        if not any(c.isupper() for c in pwd):
            errors.append('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in pwd):
            errors.append('Password must contain at least one lowercase letter')
        if not any(c in "!@#$%^&" for c in pwd):
            errors.append('Password must contain at least one special character (!@#$%^&)')
        if len(pwd) <8 or len(pwd) >128:
            errors.append('Password must contain at least 8 characters and less than or equals to 128' )

        # TODO: common passwords
        if errors:
            raise ValidationError(". ".join(errors))


        return pwd

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())

