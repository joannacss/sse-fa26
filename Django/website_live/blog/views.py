from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from blog.models import User
from blog.forms import RegisterForm, LoginForm


# Create your views here.
def index(request):
    name = "SSE-FA26"
    nickname = "JCSS"
    return render(request, 'blog/index.html', context={'name': name, 'nickname': nickname})


def register(request):
    # TODO lets use forms.py to create a form for user registration
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('blog:index'))

    return render(request, "blog/register.html", context={'form': form})


def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.get(username=username)
            if user and check_password(password, user.password):
                request.session ['user'] = username
                return redirect(reverse('blog:index'))
            else:
                form.add_error('password', 'Incorrect combination of username/password')

    return render(request, "blog/login.html", {'form': form})


def logout(request):
    pass


def create_post(request):
    pass


def view_post(request, post_id):
    pass


def list_posts(request):
    pass
