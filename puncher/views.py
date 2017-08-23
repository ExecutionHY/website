from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext

# Create your views here.


def puncher_home(request):

	ctx = {}

	return render_to_response(
		'puncher_home.html',
		ctx,
		context_instance=RequestContext(request)
	)