"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'xnews.views.xnews_home', name='xnews_home'),
    url(r'^login/$', 'xnews.views.xnews_login', name='xnews_login'),
    url(r'^register/$', 'xnews.views.xnews_register', name='xnews_register'),
    url(r'^logout/$', 'xnews.views.xnews_logout', name='xnews_logout'),
    url(r'^setting/$', 'xnews.views.xnews_setting', name='xnews_setting'),

    url(r'^category/(?P<pk>\d+)/$', 'xnews.views.xnews_category', name='xnews_category'),
    url(r'^post/(?P<pk>\d+)/$', 'xnews.views.xnews_post', name='xnews_post'),

]
