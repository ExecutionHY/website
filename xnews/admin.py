from django.contrib import admin
from .models import User, UserAdmin, Category, CategoryAdmin, PrivateCategory, PrivateCategoryAdmin, Post, PostAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PrivateCategory, PrivateCategoryAdmin)
admin.site.register(Post, PostAdmin)
