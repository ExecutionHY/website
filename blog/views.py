from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from blog.models import Post, Category

# Create your views here.


def blog_home(request):
    posts = Post.objects.all()

    ctx = {
        "posts": posts,
    }

    return render_to_response(
        'blog_home.html',
        ctx,
        context_instance=RequestContext(request)
    )


def blog_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    ctx = {
        "post": post,
    }

    return render_to_response(
        'blog_post.html',
        ctx,
        context_instance=RequestContext(request)
    )