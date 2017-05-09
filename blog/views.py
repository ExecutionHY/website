from django.shortcuts import render, render_to_response
from django.template import RequestContext
from blog.models import Post, Category

# Create your views here.


def blog(request):
    posts = Post.objects.all()

    ctx = {
        "posts": posts,
    }

    return render_to_response(
        'blog.html',
        ctx,
        context_instance=RequestContext(request)
    )