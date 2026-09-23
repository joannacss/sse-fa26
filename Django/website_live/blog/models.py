from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(unique=True,max_length=150)
    password = models.CharField()
    email = models.EmailField(unique=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
