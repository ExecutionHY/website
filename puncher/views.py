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


def puncher_daily(request):

	day0 = [1, 2]
	day1 = [0, 1]

	days = [
		day0,
		day1,
	]
	dates = [
		'Aug 22',
		'Aug 23',
	]

	ctx = {
		'user': 'email@mail.com',
		'days': days,
		'dates': dates,
	}

	return render_to_response(
		'puncher_daily.html',
		ctx,
		context_instance=RequestContext(request)
	)