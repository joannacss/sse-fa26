from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from blog.models import User, Post
from blog.forms import RegisterForm, LoginForm, PostForm


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
            request.session.cycle_key()
            request.session["user"] = form.user.username
            return redirect(reverse('blog:index'))

    return render(request, "blog/login.html", {'form': form})


def logout(request):
    #TODO: wipe the session and rotate session key
    request.session.flush()
    return redirect(reverse('blog:login'))


def create_post(request):
    user = request.get("user", None)
    if not  user:
        return redirect("blog:index")
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.user = User.objects.get(username=user)
            post.save()
            return redirect(reverse('blog:list_posts'))

    return render(request, "blog/create.html", {'form': form})


def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/view.html", {'post': post})


def list_posts(request):
    posts = Post.objects.all()
    return render(request, "blog/list.html", {'posts': posts})