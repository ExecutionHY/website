from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext


def guitarist_home(request):

	ctx = {}

	return render_to_response(
		'guitarist_home.html',
		ctx,
		context_instance=RequestContext(request)
	)