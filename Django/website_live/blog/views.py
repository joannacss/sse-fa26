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
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponse("all good, yay")#redirect(reverse("blog:login"))
    return render(request, "blog/register.html", {"form": form})


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
