from django.shortcuts import render , redirect ,get_object_or_404
from .models import Post
from .forms import PostForm
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

def post_create(request):

    if request.method == "POST":
        
        form = PostForm(request.POST)
        print("Raw POST:", request.POST)


        if form.is_valid():
            post = form.save()
            print("Cleaned data:", form.cleaned_data)
            return redirect("post_detail" , slug = post.slug)

    else:
        print("GET REQUQST")
        form = PostForm()

    return render(
        request ,
        'core/post_create.html',

        {
            "form":form
        }
    )

def post_edit(request , slug):
    post = get_object_or_404(Post , slug = slug)
    print("Database title:", post.title)
    print("Database content:", post.content)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        print("Form valid:", form.is_valid())

        if form.is_valid():
            saved_post = form.save()

            print("Form title:", form.cleaned_data["title"])
            print("Saved object title:", saved_post.title)
            print("Saved object ID:", saved_post.id)


            saved_post.refresh_from_db()

            print("Database title:", saved_post.title)
            print("Database ID:", saved_post.id)



            return redirect("post_detail" , slug = post.slug)
        else:
            print("Form errors:", form.errors)
    else:
        form = PostForm(instance=post)

    context={
        "form": form,
        "post": post,
    }

    return render (request , "core/post_edit.html", context)