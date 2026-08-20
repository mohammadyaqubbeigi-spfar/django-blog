from django.shortcuts import render , get_object_or_404
from .models import Post
from django.core.paginator import Paginator
from django.db.models import Q

def home (request) :

    query = request.GET.get("q")
    sort = request.GET.get("sort", "newest")

    posts = Post.objects.all()

    sort_options = {
        "newest": "-created_at",
        "oldest": "created_at",
        "title": "title",
    }
    order = sort_options.get(sort, "-created_at")

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    posts = posts.order_by(order)
    
    paginator = Paginator(posts, 2)
    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    params = request.GET.copy()
    params.pop("page",None)

    next_query = None
    previous_query = None
    
    if page_obj.has_next():
        next_params = params.copy()
        next_params["page"] = page_obj.next_page_number()
        next_query = next_params.urlencode()

    if page_obj.has_previous():
        previous_params = params.copy()
        previous_params["page"] = page_obj.previous_page_number()
        previous_query = previous_params.urlencode()

    context ={
        "title" : "my blog",
        "page_obj": page_obj,
        "query":query,
        "sort": sort,
        "next_query": next_query,
        "previous_query": previous_query,
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