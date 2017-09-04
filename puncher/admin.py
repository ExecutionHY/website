from django.contrib import admin
from .models import User, UserTask, DailyTask, UserAdmin, UserTaskAdmin, DailyTaskAdmin
from .models import Checkpoint, CheckpointAdmin, Payment, PaymentAdmin, PaymentKind, PaymentKindAdmin
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(UserTask, UserTaskAdmin)
admin.site.register(DailyTask, DailyTaskAdmin)
admin.site.register(Checkpoint, CheckpointAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentKind, PaymentKindAdmin)