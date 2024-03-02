from django.shortcuts import render,get_object_or_404
from blog.models import  Blog
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import  Q


# Create your views here.




def show_blog(request, search_result=None):

    article = Blog.objects.all()
    news = article[:5]
    if search_result is not None:
        article = search_result
    paginator = Paginator(article,9)
    page = request.GET.get("page")
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects =  paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request, "show_blog.html", {"pages":objects,"paginator":paginator,"news":news})
    


def show_detail(request,slug_blog):
    blog_detail = get_object_or_404(Blog,slug=slug_blog)
    article = Blog.objects.all()
    news = article[:5]
    return render(request,"show_detail.html", {"blog_detail":blog_detail,"news":news})





def search_blog(request):
    search_blog = request.GET.get("q")

    if search_blog:


        find_blogs = Blog.objects.filter(Q(title__icontains=search_blog) | Q(body__icontains=search_blog))
        return show_blog(request,find_blogs)
    else:
        return show_blog(request)    

