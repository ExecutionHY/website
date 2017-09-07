from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import datetime
from django import forms

from models import User, UserTask, DailyTask, Checkpoint, Payment, PaymentKind


# Create your views here.


def puncher_home(request):
	# get the first user -- Execution
	user = User.objects.first()

	# ------- get some example display

	# tasks for recent 6 days, divided by day
	tasks = DailyTask.objects.filter(user=user)
	today = datetime.date.today()
	days = []   # each day include some tasks
	dates = []
	for i in range(5, -1, -1):
		this_day = today - datetime.timedelta(days=i)
		day = tasks.filter(date__year=this_day.year, date__month=this_day.month, date__day=this_day.day)
		days.append(day)
		dates.append(this_day)

	# money
	checkpoint = Checkpoint.objects.filter(user=user).last()
	amount = checkpoint.wechat + checkpoint.alipay + checkpoint.campus
	payments_after_check = Payment.objects.filter(user=user, time__gt=checkpoint.time)
	for payment in payments_after_check:
		amount += payment.value

	today = datetime.date.today()
	payments_this_month = Payment.objects.filter(user=user, time__year=today.year, time__month=today.month)
	kind_list = PaymentKind.objects.all()

	bills = [0] * kind_list.last().id
	monthly_in = 0
	monthly_out = 0
	for payment in payments_this_month:
		if payment.value < 0:
			bills[payment.kind.id - 1] += payment.value
			monthly_out += payment.value
		else:
			monthly_in += payment.value

	bill_list = []
	for i in range(kind_list.last().id):
		if monthly_out == 0:
			percentage = 0
		else:
			percentage = bills[i] / monthly_out * 100

		if bills[i] < 0:
			bill = {
				'kind': PaymentKind.objects.get(id=i + 1),
				'index': i,
				'sum': -bills[i],
				'percentage': percentage,
			}
			bill_list.append(bill)

	# ------ end of example display

	# deal with login request
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = User.objects.filter(email=email)
		if user:
			if user.first().password == password:
				return HttpResponseRedirect('/puncher/daily/?uid=' + user.first().id.__str__() + '&pwd=' + password)
		msg = "login failed"

	else:
		msg = None

	ctx = {
		'days': days,
		'dates': dates,

		'monthly_in': monthly_in,
		'monthly_out': monthly_out,
		'kind_list': kind_list,
		'bill_list': bill_list,
		'today': today,
		'msg': msg,
	}

	return render_to_response(
		'puncher_home.html',
		ctx,
		context_instance=RequestContext(request)
	)


formats = ['%Y-%m-%d %H:%M',  # '2006-10-25 14:30:59'
           ]


class PaymentForm(forms.Form):
	info = forms.CharField(label='info', max_length=64)
	value = forms.FloatField(label='value')
	kind = forms.CharField(label='kind', max_length=64)
	time = forms.DateTimeField(label='time', input_formats=formats)


class CheckpointForm(forms.Form):
	wechat = forms.FloatField()
	alipay = forms.FloatField()
	campus = forms.FloatField()


def puncher_daily(request):

	# get user
	if 'uid' in request.GET:
		uid = request.GET.get('uid')
		pwd = request.GET.get('pwd')
		user = User.objects.filter(id=uid).first()
		# check password
		if user.password != pwd:
			user = None
			uid = -1
	else:
		user = None
		uid = -1
		pwd = None

	# tasks for recent 6 days, divided by day
	tasks = DailyTask.objects.filter(user=user)
	today = datetime.date.today()
	days = []   # each day include some tasks
	dates = []
	for i in range(5, -1, -1):
		this_day = today - datetime.timedelta(days=i)
		day = tasks.filter(date__year=this_day.year, date__month=this_day.month, date__day=this_day.day)
		days.append(day)
		dates.append(this_day)

	# to_do list for today
	todo_list = []
	my_tasks = UserTask.objects.filter(user=user)
	for task in my_tasks:
		last_task = tasks.filter(taskNo=task.number).last()
		if last_task is None:
			delta = task.interval
		else:
			last_date = last_task.date.date()
			delta = (today - last_date).days

		todo = {
			'task': task,
			'delta': delta,
		}
		todo_list.append(todo)

	todo_list = sorted(todo_list, key=lambda todo: -float(todo['delta'] / float(todo['task'].interval)))

	# get current money amount
	checkpoint = Checkpoint.objects.filter(user=user).last()
	amount = checkpoint.wechat + checkpoint.alipay + checkpoint.campus
	payments_after_check = Payment.objects.filter(user=user, time__gt=checkpoint.time)
	for payment in payments_after_check:
		amount += payment.value

	# get the data of this month
	payments_this_month = Payment.objects.filter(user=user, time__year=today.year, time__month=today.month)

	# the last kind is list on the top
	# sum up money-in & out for this month
	last_kind_id = PaymentKind.objects.last().id
	bills = [0] * last_kind_id
	monthly_in = 0
	monthly_out = 0
	for payment in payments_this_month:
		if payment.value < 0:
			bills[payment.kind.id - 1] += payment.value
			monthly_out += payment.value
		else:
			monthly_in += payment.value

	# build a list for template to use
	bill_list = []
	for i in range(last_kind_id):
		if monthly_out == 0:
			percentage = 0
		else:
			percentage = bills[i] / monthly_out * 100

		if bills[i] < 0:
			bill = {
				'kind': PaymentKind.objects.get(id=i + 1),
				'index': i,
				'sum': -bills[i],
				'percentage': percentage,
			}
			bill_list.append(bill)

	# deal with request of adding payment & checkpoint
	if request.method == 'POST':
		new_taskNo = request.POST.get('taskNo')
		if new_taskNo:
			DailyTask.objects.create(user=user, taskNo=new_taskNo)
			# refresh the page
			return HttpResponseRedirect('?uid=' + uid + '&pwd=' + pwd)

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

			# refresh the page
			return HttpResponseRedirect('?uid=' + uid + '&pwd=' + pwd)

		# another kind of form
		else:
			form = CheckpointForm(request.POST)

			if form.is_valid():
				# get payment data
				wechat = form.cleaned_data['wechat']
				alipay = form.cleaned_data['alipay']
				campus = form.cleaned_data['campus']

				# create new checkpoint
				Checkpoint.objects.create(user=user, wechat=wechat, alipay=alipay, campus=campus)
				# create a patch payment
				amount_current = wechat + alipay + campus
				if amount_current != amount:
					kind_patch = PaymentKind.objects.get(kind="other")
					Payment.objects.create(user=user, info="patch", value=amount_current - amount,
					                       kind=kind_patch, time=datetime.datetime.now())
				# refresh
				return HttpResponseRedirect('?uid=' + uid + '&pwd=' + pwd)

	ctx = {
		'user': user,
		'days': days,
		'dates': dates,
		'todo_list': todo_list,

		'amount': amount,
		'monthly_in': monthly_in,
		'monthly_out': monthly_out,
		'kind_list': PaymentKind.objects.all(),
		'bill_list': bill_list,
		'today': today,

		'last_wechat': checkpoint.wechat,
		'last_alipay': checkpoint.alipay,
		'last_campus': checkpoint.campus,
	}

	return render_to_response(
		'puncher_daily.html',
		ctx,
		context_instance=RequestContext(request)
	)
