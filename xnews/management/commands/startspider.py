# coding: utf-8
from django.core.management import BaseCommand
import time

# for spider
import requests
from bs4 import BeautifulSoup
from ...models import Category, Post


def spider():

    def getlist_sina(url):
        # get html
        htmldata = requests.get(url).text
        # parse the html
        soup = BeautifulSoup(htmldata,'html.parser')
        # return a list of <a>
        tags = soup.select("div.blk121 > a")

        linklist = []
        for tag in tags:
            link = tag.get("href")
            linklist.append(link)

        tags = soup.select("div.blk122 > a")
        for tag in tags:
            link = tag.get("href")
            linklist.append(link)

        return linklist

    def getpost_sina(url):
        print url
        response = requests.get(url)
        response.encoding = 'utf-8'
        htmldata = response.text
        soup = BeautifulSoup(htmldata, 'html.parser')

        head = soup.select("div.page-header > h1")
        time_source = soup.select("span.time-source")
        body = soup.select("div.article")

        post = {
            'title': head[0].get_text(),
            'time_source': time_source[0].get_text(),
            'body': body[0]
        }

        return post

    def getlist_sohu(url):
        # get html
        htmldata = requests.get(url).text
        # parse the html
        soup = BeautifulSoup(htmldata,'html.parser')
        # return a list of <a>
        tags = soup.select("div.news-box > h4 > a")

        linklist = []
        for tag in tags:
            link = tag.get("href")
            linklist.append(link)

        return linklist

    def getpost_sohu(url):
        print url
        response = requests.get(url)
        response.encoding = 'utf-8'
        htmldata = response.text
        soup = BeautifulSoup(htmldata, 'html.parser')

        head = soup.select("div.text-title > h1")
        time_source = soup.select("div.article-info")
        body = soup.select("article.article")

        post = {
            'title': head[0].get_text(),
            'time_source': time_source[0].get_text(),
            'body': body[0]
        }

        return post

    def getlist_ifeng(url):
        # get html
        htmldata = requests.get(url).text
        # parse the html
        soup = BeautifulSoup(htmldata,'html.parser')
        # return a list of <a>
        tags = soup.select("div.w920 > h1 > a")

        linklist = []
        for tag in tags:
            link = tag.get("href")
            linklist.append(link)

        tags = soup.select("div.juti_list > h3 > a")
        for tag in tags:
            link = tag.get("href")
            linklist.append(link)

        return linklist

    def getpost_ifeng(url):
        print url
        response = requests.get(url)
        response.encoding = 'utf-8'
        htmldata = response.text
        soup = BeautifulSoup(htmldata, 'html.parser')

        head = soup.select("div.left > div > h1")
        time_source = soup.select("p.p_time")
        body = soup.select("div.js_selection_area")
        post = {
            'title': head[0].get_text(),
            'time_source': time_source[0].get_text(),
            'body': body[0]
        }

        return post

    def getlist_huanqiu(url):
        # get html
        htmldata = requests.get(url).text
        # parse the html
        soup = BeautifulSoup(htmldata,'html.parser')
        # return a list of <a>
        tags = soup.select("ul.listDot-box > li > a")

        linklist = []
        for tag in tags:
            link = tag.get("href")
            linklist.append(link)

        tags = soup.select("ul.list-box > li > a")
        for tag in tags:
            link = tag.get("href")
            linklist.append(link)

        return linklist

    def getpost_huanqiu(url):
        print url
        response = requests.get(url)
        response.encoding = 'utf-8'
        htmldata = response.text
        soup = BeautifulSoup(htmldata, 'html.parser')

        head = soup.select("div.conText > h1")
        pubtime = soup.select("strong.timeSummary")
        source = soup.select("strong.fromSummary")
        body = soup.select("div.text")
        post = {
            'title': head[0].get_text(),
            'time_source': pubtime[0].get_text() + source[0].get_text(),
            'body': body[0]
        }

        return post
    """
    # spider for sina-china
    category = Category.objects.get(pk=1)
    Post.objects.filter(category=category).delete()
    linklist = getlist_sina('http://news.sina.com.cn/china/')
    for link in linklist:
        post = getpost_sina(link)
        Post.objects.create(title=post.get('title'),
                            time_source=post.get('time_source'),
                            body=post.get('body'),
                            category=category
                            )
    print '---'
    # spider for sina-world
    category = Category.objects.get(pk=2)
    Post.objects.filter(category=category).delete()
    linklist = getlist_sina('http://news.sina.com.cn/world/')
    for link in linklist:
        post = getpost_sina(link)
        Post.objects.create(title=post.get('title'),
                            time_source=post.get('time_source'),
                            body=post.get('body'),
                            category=category
                            )
    print '---'
    # spider for sina-society
    category = Category.objects.get(pk=3)
    Post.objects.filter(category=category).delete()
    linklist = getlist_sina('http://news.sina.com.cn/society/')
    for link in linklist:
        post = getpost_sina(link)
        Post.objects.create(title=post.get('title'),
                            time_source=post.get('time_source'),
                            body=post.get('body'),
                            category=category
                            )
    print '---'
    # spider for 163-war
    category = Category.objects.get(pk=4)
    Post.objects.filter(category=category).delete()
    linklist = getlist_sohu('http://mil.sohu.com/')
    for link in linklist:
        post = getpost_sohu('http:'+link)
        Post.objects.create(title=post.get('title'),
                            time_source=post.get('time_source'),
                            body=post.get('body'),
                            category=category
                            )

    # spider for ifeng-taiwan
    category = Category.objects.get(pk=5)
    Post.objects.filter(category=category).delete()
    linklist = getlist_ifeng('http://news.ifeng.com/taiwan/')
    for link in linklist:
        post = getpost_ifeng(link)
        Post.objects.create(title=post.get('title'),
                            time_source=post.get('time_source'),
                            body=post.get('body'),
                            category=category
                            )
"""
    # spider for huanqiu-ent
    category = Category.objects.get(pk=6)
    Post.objects.filter(category=category).delete()
    linklist = getlist_huanqiu('http://ent.huanqiu.com/')
    for link in linklist:
        post = getpost_huanqiu(link)
        Post.objects.create(title=post.get('title'),
                            time_source=post.get('time_source'),
                            body=post.get('body'),
                            category=category
                            )


# The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "this command will start my spider system"

    # A command must define handle()
    def handle(self, *args, **options):
        spider()
        """
        while True:
            spider()
            time.sleep(3)
        """