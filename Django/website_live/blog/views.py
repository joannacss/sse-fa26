from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from blog.forms import RegisterForm, LoginForm, PostForm
from blog.models import User, Post


# Create your views here.
def index(request):
    name = "SSE-FA26"
    nickname = "JCSS"
    return render(request, 'blog/index.html', context={'name': name, 'nickname': nickname})


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('blog:login'))

    return render(request, "blog/register.html", context={'form': form})


def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            request.session.cycle_key()
            request.session["user"] = form.user.username
            return redirect(reverse('blog:list_posts'))

    return render(request, "blog/login.html", {'form': form})


def logout(request):
    #TODO: wipe the session, redirect to login
    pass


def create_post(request):
    if "user" not in request.session:
        return redirect("blog:list_posts")
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.user = User.objects.get(username=request.session["user"])
            post.save()
            return redirect(reverse('blog:list_posts'))

    return render(request, "blog/create.html", {'form': form})


def view_post(request, post_id):
    pass



def list_posts(request):
    pass