from django.shortcuts import render

# Create your views here.
def index(request):
    name = "SSE-FA26"
    nickname = "JCSS"
    return render(request, 'blog/index.html', context={'name': name, 'nickname': nickname})

def register(request):
    return render(request, 'blog/register.html')