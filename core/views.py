from django.shortcuts import render , get_object_or_404
from .models import Post
from django.core.paginator import Paginator
from django.db.models import Q

def home (request) :

    query = request.GET.get("q")

    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    
    paginator = Paginator(posts, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context ={
        "title" : "my blog",
        "page_obj": page_obj,
        "query":query, 
    }
    return render (request,'core/home.html', context)

def post_detail(request , slug):
    post = get_object_or_404(Post ,slug = slug)

    page = request.GET.get("page")
    query = request.GET.get("q")

    context ={
        "post":post,
        "page":page,
        "query":query,
    }
    return render(request , 'core/post_detail.html', context)