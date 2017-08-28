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

	# get user
	request.encoding = 'utf-8'
	uid = request.GET.get('uid', 1)
	if uid is None:
		user = User.objects.first()
	else:
		user = User.objects.filter(id=uid).first()

	# tasks for recent 6 days, divided by day
	tasks = DailyTask.objects.filter(user=user)
	today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
	today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
	today = datetime.date.today()
	days = []
	dates = []
	for i in range(5, -1, -1):
		this_min = today_min - datetime.timedelta(days=i)
		this_max = today_max - datetime.timedelta(days=i)
		this_day = today - datetime.timedelta(days=i)
		day = tasks.filter(date__range=(this_min, this_max))
		days.append(day)
		dates.append(this_day)

	# to_do list for today
	todo_list = []
	my_tasks = UserTask.objects.filter(user=user)
	for task in my_tasks:
		last_task = tasks.filter(taskNo=task.number).last()
		if last_task is None:
			delta = 0
		else:
			last_date = last_task.date.date()
			delta = (today - last_date).days

		todo = {
			'task': task,
			'delta': delta,
		}
		todo_list.append(todo)

	todo_list = sorted(todo_list, key=lambda todo: -float(todo['delta']/float(todo['task'].interval)))

	ctx = {
		'user': user,
		'days': days,
		'dates': dates,
		'todo_list': todo_list,
	}

	return render_to_response(
		'puncher_daily.html',
		ctx,
		context_instance=RequestContext(request)
	)