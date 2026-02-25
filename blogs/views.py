from django.shortcuts import render

from blogs.models import Blog, BlogStatus, Category, Tag


def blog_detail_page_view(request, pk):
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        render(request,'shared/404.html')

    context = {
        "blog":blog
    }
    return render(
        request, 'blogs/blog-detail.html',context=context
    )


def blog_list_page_view(request):
    context = {
        "blogs": Blog.objects.filter(status=BlogStatus.PUBLISHED),
        "categories":Category.objects.filter(parent=None),
        "tags":Tag.objects.all(),
        "recent_posts":Blog.objects.order_by('-created_at')[:2]
    }
    return render(request, 'blogs/blogs-list.html',context)
