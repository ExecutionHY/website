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

    def getlist_163(url):
        # get html
        htmldata = requests.get(url).text
        # parse the html
        soup = BeautifulSoup(htmldata,'html.parser')
        # return a list of <a>
        tags = soup.select("div.news_title")
        print htmldata

        linklist = []
        for tag in tags:
            link = tag.get("href")
            linklist.append(link)

        return linklist

    def getpost_163(url):
        print url
        response = requests.get(url)
        response.encoding = 'utf-8'
        htmldata = response.text
        soup = BeautifulSoup(htmldata, 'html.parser')

        head = soup.select("div.post_content_main > h1")
        time_source = soup.select("div.post_time_source")
        body = soup.select("div.post_text")

        post = {
            'title': head[0].get_text(),
            'time_source': time_source[0].get_text(),
            'body': body[0]
        }

        return post

    def getlist_xinhua(url):
        # get html
        htmldata = requests.get(url).text
        # parse the html
        soup = BeautifulSoup(htmldata,'html.parser')
        # return a list of <a>
        tags = soup.select("ul.newList01 > li > a")

        linklist = []
        for tag in tags:
            link = tag.get("href")
            linklist.append(link)

        return linklist

    def getpost_xinhua(url):
        print url
        response = requests.get(url)
        response.encoding = 'utf-8'
        htmldata = response.text
        soup = BeautifulSoup(htmldata, 'html.parser')

        head = soup.select("div.h-title")
        time_source = soup.select("div.h-info")
        body = soup.find(id="p-detail")

        # some web is not formed normally
        if len(head) > 0:
            post = {
                'title': head[0].get_text(),
                'time_source': time_source[0].get_text(),
                'body': body
            }
        else:
            post = None
        return post

    categories = Category.objects.all()
    for category in categories:
        Post.objects.filter(category=category).delete()

        # spider for sina
        linklist = getlist_sina(category.url_sina)
        for link in linklist:
            post = getpost_sina(link)
            Post.objects.create(title=post.get('title'),
                                time_source=post.get('time_source'),
                                body=post.get('body'),
                                category=category
                                )

        linklist = getlist_xinhua(category.url_xinhua)
        for link in linklist:
            post = getpost_xinhua(link)
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