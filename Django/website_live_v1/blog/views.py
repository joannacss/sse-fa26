from django import forms
from django.shortcuts import render

from blog.models import User


# Create your views here.
def index(request):
    return render(request, 'blog/index.html')

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
def register(request):
    form = RegistrationForm( request.POST or None)
    context = {"form": form}
    if request.method == 'POST':
        # Handle registration logic here
        pass
    return render(request, 'blog/register.html', context)