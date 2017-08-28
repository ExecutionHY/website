from django.db import models
from django.contrib import admin

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
