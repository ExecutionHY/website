# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Category(models.Model):
    category = models.CharField(u"category", max_length=128)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.category

    @models.permalink
    def get_absolute_url(self):
        return 'category', (), {'pk': self.pk}


class Tag(models.Model):
    tag = models.CharField(u"tag", max_length=128)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.tag

    @models.permalink
    def get_absolute_url(self):
        return 'tag', (), {'pk': self.pk}


class Post(models.Model):
    title = models.CharField(u"title", max_length=128)
    author = models.ForeignKey(User)
    publication_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    content = models.TextField(u"content")
    category = models.ForeignKey(Category, verbose_name='category')
    tags = models.ManyToManyField(Tag, blank=False, null=False)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'post', (), {'pk': self.pk}


class PostAdmin(admin.ModelAdmin):
    title = models.ForeignKey(Post, verbose_name='title')
    publication_date = models.ForeignKey(Post, verbose_name='publication_date')
    category = models.ForeignKey(Post, verbose_name='category')
    list_display = ('title', 'publication_date', 'category')


class CategoryAdmin(admin.ModelAdmin):
    category = models.ForeignKey(Category, verbose_name='category')
    list_display = ('category',)


class TagAdmin(admin.ModelAdmin):
    tag = models.ForeignKey(Tag, verbose_name='tag')
    list_display = ('tag', )