from django.contrib import admin
from .models import User, UserTask, DailyTask, UserAdmin, UserTaskAdmin, DailyTaskAdmin
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(UserTask, UserTaskAdmin)
admin.site.register(DailyTask, DailyTaskAdmin)