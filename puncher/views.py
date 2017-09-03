from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import datetime
from django import forms

from models import User, UserTask, DailyTask, CheckPoint, Payment, PaymentKind

# Create your views here.


def puncher_home(request):

	ctx = {}

	return render_to_response(
		'puncher_home.html',
		ctx,
		context_instance=RequestContext(request)
	)

formats = ['%Y-%m-%d %H:%M',    # '2006-10-25 14:30:59'
]


class PaymentForm(forms.Form):
	info = forms.CharField(label='info', max_length=64)
	value = forms.FloatField(label='value')
	kind = forms.CharField(label='kind', max_length=64)
	time = forms.DateTimeField(label='time', input_formats=formats)


def puncher_daily(request):

	# get user
	if 'uid' in request.GET:
		uid = request.GET.get('uid')
		user = User.objects.filter(id=uid).first()
	else:
		user = None

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
	todo_count = 0
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
		todo_count += 1

	todo_list = sorted(todo_list, key=lambda todo: -float(todo['delta']/float(todo['task'].interval)))

	# money management
	checkpoint = CheckPoint.objects.filter(user=user).last()
	amount = checkpoint.wechat + checkpoint.alipay + checkpoint.campus
	payments_after_check = Payment.objects.filter(user=user, time__gt=checkpoint.time)
	for payment in payments_after_check:
		amount += payment.value

	kind_list = PaymentKind.objects.all()

	if request.method == 'POST':
		form = PaymentForm(request.POST)
		if form.is_valid():
			# get payment data
			info = form.cleaned_data['info']
			value = form.cleaned_data['value']
			kind_str = form.cleaned_data['kind']
			kind = PaymentKind.objects.get(kind=kind_str)
			time = form.cleaned_data['time']

			# create new payment
			Payment.objects.create(user=user, info=info, value=value, kind=kind, time=time)

			return HttpResponseRedirect('?uid='+uid)

	ctx = {
		'user': user,
		'days': days,
		'dates': dates,
		'todo_list': todo_list,
		'todo_count': todo_count,
		'amount': amount,
		'kind_list': kind_list,
		'today': today,
	}

	return render_to_response(
		'puncher_daily.html',
		ctx,
		context_instance=RequestContext(request)
	)