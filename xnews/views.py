from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

# Create your views here.


def xnews_home(request):

    ctx = [
        
    ]

    return render_to_response(
        'xnews_home.html',
        ctx,
        context_instance=RequestContext(request)
    )

