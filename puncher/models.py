from django.db import models
from django.contrib import admin

from django import forms

# Create your models here.


class User(models.Model):
	email = models.EmailField()
	password = models.CharField(max_length=64)

	class Meta:
		ordering = ['-id']

	def __unicode__(self):
		return str(self.email)


class UserTask(models.Model):
	user = models.ForeignKey(User, verbose_name="email")
	task = models.CharField(max_length=64)
	interval = models.IntegerField(default=1)
	number = models.CharField(max_length=1)

	class Meta:
		ordering = ['-id']

	def __unicode__(self):
		return str(self.id)


class DailyTask(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, verbose_name="email")
	taskNo = models.CharField(max_length=1)

	class Meta:
		ordering = ['-id']

	def __unicode__(self):
		return str(self.id)


class UserAdmin(admin.ModelAdmin):
	email = models.ForeignKey(User, verbose_name="email")
	list_display = ('email', )


class UserTaskAdmin(admin.ModelAdmin):
	user = models.ForeignKey(UserTask, verbose_name="user")
	task = models.ForeignKey(UserTask, verbose_name="task")
	interval = models.ForeignKey(UserTask, verbose_name="interval")
	number = models.ForeignKey(UserTask, verbose_name="number")
	list_display = ('user', 'task', 'interval', 'number')


class DailyTaskAdmin(admin.ModelAdmin):
	date = models.ForeignKey(DailyTask, verbose_name="date")
	user = models.ForeignKey(DailyTask, verbose_name="user")
	taskNo = models.ForeignKey(DailyTask, verbose_name="taskNo")
	list_display = ('date', 'user', 'taskNo')


class CheckPoint(models.Model):
	user = models.ForeignKey(User, verbose_name="email")
	wechat = models.FloatField(default=0)
	alipay = models.FloatField(default=0)
	campus = models.FloatField(default=0)
	time = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
	user = models.ForeignKey(User, verbose_name="email")
	info = models.CharField(max_length=64)
	value = models.FloatField(default=0)
	time = models.DateField()


class CheckPointAdmin(admin.ModelAdmin):
	user = models.ForeignKey(CheckPoint, verbose_name="email")
	wechat = models.ForeignKey(CheckPoint, verbose_name="wechat")
	alipay = models.ForeignKey(CheckPoint, verbose_name="alipay")
	campus = models.ForeignKey(CheckPoint, verbose_name="campus")
	time = models.ForeignKey(CheckPoint, verbose_name="time")
	list_display = ('user', 'wechat', 'alipay', 'campus', 'time')

formats = ['%Y-%m-%d',      # '2006-10-25'
	'%m/%d/%Y',       # '10/25/2006'
	'%m/%d/%y']       # '10/25/06'


class PaymentAdmin(admin.ModelAdmin):
	user = models.ForeignKey(Payment, verbose_name="email")
	info = models.ForeignKey(Payment, verbose_name="info")
	value = models.ForeignKey(Payment, verbose_name="value")
	time = forms.DateField(input_formats=formats)
	list_display = ('user', 'info', 'value', 'time')