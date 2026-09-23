from django.shortcuts import render


# Create your views here.
def index(request):
    name = "SSE-FA26"
    nickname = "JCSS"
    return render(request, 'blog/index.html', context={'name': name, 'nickname': nickname})


def register(request):
    return render(request, 'blog/register.html')


def login(request):
    pass


def logout(request):
    pass


def create_post(request):
    pass


def view_post(request, post_id):
    pass


def list_posts(request):
    pass
