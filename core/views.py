from django.shortcuts import render
from .models import Post

def home (request) :
    posts = Post.objects.all()

    context ={
        "title" : "my blog",
        "posts": posts, 
    }
    return render (request,'core/home.html', context)
