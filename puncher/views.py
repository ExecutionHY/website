from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import datetime

from models import User, UserTask, DailyTask

# Create your views here.


def puncher_home(request):

	ctx = {}

	return render_to_response(
		'puncher_home.html',
		ctx,
		context_instance=RequestContext(request)
	)


def puncher_daily(request):

	request.encoding = 'utf-8'
	uid = request.GET.get('uid', 1)
	if uid is None:
		user = User.objects.first()
	else:
		user = User.objects.filter(id=uid).first()

	tasks = DailyTask.objects.filter(user=user)

	# tasks for recent 6 days, divided by day
	today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
	today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
	days = []
	dates = []
	for i in range(5, -1, -1):
		this_min = today_min - datetime.timedelta(days=i)
		this_max = today_max - datetime.timedelta(days=i)
		this_day = datetime.date.today() - datetime.timedelta(days=i)
		day = tasks.filter(date__range=(this_min, this_max))
		days.append(day)
		dates.append(this_day)

	ctx = {
		'user': user,
		'days': days,
		'dates': dates,
	}

	return render_to_response(
		'puncher_daily.html',
		ctx,
		context_instance=RequestContext(request)
	)