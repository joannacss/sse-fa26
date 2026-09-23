import re

from django import forms
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

from blog.models import User


class RegisterForm(forms.ModelForm):
    pass



