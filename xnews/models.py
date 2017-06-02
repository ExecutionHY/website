from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.forms import ModelForm

# Create your models here.


class Category(models.Model):
    category = models.CharField(u"category", max_length=128)
    source = models.CharField(max_length=128, default='')

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.category

    @models.permalink
    def get_absolute_url(self):
        return 'category', (), {'pk': self.pk}


class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    introduction = models.CharField(max_length=128, default='This guy is too lazy to left anything.')

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.email


class PrivateCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name='category')
    email = models.ForeignKey(User, verbose_name='email')
    count = models.FloatField(default='1000')

    def __unicode__(self):
        return self.id


class CategoryAdmin(admin.ModelAdmin):
    category = models.ForeignKey(Category, verbose_name='category')
    list_display = ('category',)


class UserAdmin(admin.ModelAdmin):
    email = models.ForeignKey(User, verbose_name='email')
    list_display = ('email',)


class PrivateCategoryAdmin(admin.ModelAdmin):
    email = models.ForeignKey(PrivateCategory, verbose_name='email')
    category = models.ForeignKey(PrivateCategory, verbose_name='category')
    count = models.ForeignKey(PrivateCategory, verbose_name='count')
    list_display = ('email', 'category', 'count')


class Post(models.Model):
    title = models.CharField(max_length=64)
    time_source = models.CharField(max_length=64, default='null')
    body = models.CharField(max_length=2048)
    category = models.ForeignKey(Category, verbose_name='category')

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'title', (), {'pk': self.pk}


class PostAdmin(admin.ModelAdmin):
    title = models.ForeignKey(Post, verbose_name='title')
    category = models.ForeignKey(Post, verbose_name='category')
    list_display = ('title', 'category')