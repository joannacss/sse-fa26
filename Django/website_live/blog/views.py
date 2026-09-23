from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from blog.forms import RegisterForm


# Create your views here.
def index(request):
    name = "SSE-FA26"
    nickname = "JCSS"
    return render(request, 'blog/index.html', context={'name': name, 'nickname': nickname})


def register(request):
    # TODO lets use forms.py to create a form for user registration
    return render(request, "blog/register.html")


def login(request):
    return render(request, "blog/login.html")


def logout(request):
    pass


def create_post(request):
    pass


def view_post(request, post_id):
    pass


def list_posts(request):
    pass
