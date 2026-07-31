from django.shortcuts import render , get_object_or_404
from .models import Post
from django.core.paginator import Paginator

def home (request) :
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context ={
        "title" : "my blog",
        "page_obj": page_obj, 
    }
    return render (request,'core/home.html', context)

def post_detail(request ,  post_id):
    post = get_object_or_404(Post , id = post_id)

    context ={
        "post":post
    }
    return render(request , 'core/post_detail.html', context)