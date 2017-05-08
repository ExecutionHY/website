from django.contrib import admin
from .models import Post, PostAdmin, Category, CategoryAdmin, Tag, TagAdmin
# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)