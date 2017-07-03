# Website建设

### 基本配置

Django + MySQL

### 维护工具

Pycharm

### 网站结构

Home

- Blog
- Works
- X-News

### 必要功能

- 博客：markdown
- 评论：Disqus
- 分页：
- 搜索：
- 聊天室：

参考原来的教程。[http://udn.yyuap.com/doc/django-web-app-book/index.html](http://udn.yyuap.com/doc/django-web-app-book/index.html)

### 版本控制

Pycharm的git控制 

[http://blog.csdn.net/hk2291976/article/details/51159974](http://blog.csdn.net/hk2291976/article/details/51159974)

注意commit是一次提交，但commit仅仅提交到本地，要push才能更新到github

## 1 Django的MySQL配置

参考的教程[http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-mysql-for-django](http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-mysql-for-django)

### 1.1 mac上安装mysql

[http://www.jianshu.com/p/fd3aae701db9](http://www.jianshu.com/p/fd3aae701db9)

- 官网下载community版。安装成功。

> 2017-05-05T14:30:11.268790Z 1 [Note] A temporary password is generated for root@localhost: #,6rSu+aaOdv
>
> If you lose this password, please consult the section How to Reset the Root Password in the MySQL reference manual.

- 开启server
- bash_profile中添加mysql的path。注意要重启terminal才有效
- \$ mysql -uroot -p
- \> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('password');

### 1.2 检查mysql-python连接

```
$ sudo pip install python-mysql
```

下载python-mysql。运行上述代码，再运行

```
$ python -c "import MySQLdb"
```

检查MySQLdb能否调用。失败。查了很多资料，下载这个可以解决：

```
$ sudo easy_install MySQL-Python
```

### 1.3 配置Django数据库

在终端连接mysql建立一个数据库。

```
$ mysql -uroot -p
Enter password:
> 
CREATE DATABASE website_db;
CREATE USER 'root@localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON website_db.* TO 'root@localhost';
FLUSH PRIVILEGES;
quit
```

在Django的setting里修改DATABASE设置。

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'website_db',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

同步数据库，新建一个superuser

```ba sh
$ python manage.py syncdb
```

### 1.4 关于MySQL的特点

SQLite是Unix系统自带的，新建Django系统默认的轻量级数据库，当数据访问较多的时候，需要更换至工业化的数据库。

MySQL相比它，没有数据库实体保存在目标文件夹中，也就是说备份和迁移什么的还要指令去实现。（Django自带指令实现备份与恢复  [http://blog.csdn.net/SVALBARDKSY/article/details/51433893](http://blog.csdn.net/SVALBARDKSY/article/details/51433893)）

这一点而言还是比较好的，就不会把数据库git到网上去了。

## 2 网站主页部分

这里完成网站的主题模版的编写。后面的app都调用base.html之类的模版即可。主页的话不需要startapp，就写个简单的静态页面就行了。在网上找到不错的demo扒下来。

### 2.1 templates、urls、views

先显示个"Hello Execution"页面。

- templates文件夹里面写个home.html
- urls.py 加上 / 的映射。

```python
url(r'^$', 'website.views.home', name='home'),
```

- views.py 加上home的函数

```python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


def home(request):

    return render_to_response("home.html", context_instance=RequestContext(request))
```

### 2.2 主页base编写

扒一个网页demo模版，作为base.html。home.html改成这样

```
{% extends "base.html" %}

{% block title %}Execution's Blogs{% endblock %}
{% block content %}

    Hello Execution!

{% endblock %}
```

### 2.3 网页样式css

https://html5up.net/prologue](https://html5up.net/prologue 在网上找到了一个h5的响应式网页，其排版跟我想的差不多，决定拿来套用。

把css文件什么的也给扒下来。保存在 $PROJECT_NAME/static 文件夹下。

这样子base.html还是不能调用那些css。需要setting里面设置好static的地址。增加一句

```
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
```

### 2.4 FontAwesome介绍

[http://fontawesome.io/icons/](http://fontawesome.io/icons/)

它是一种符号字体，非常适合扁平化设计中的一些图案。我们在官网把它下载下来就可以使用，或者CDN。目前我用的本地版本是4.7.0。

### 2.5 skel样式

一种神奇的排版方式，稍微摸索一下应该就懂了，两个数字貌似是占据该行的比例。

```html
<div class="8u 12u$(mobile)"></div>
<div class="4u$ 12u$(mobile)"></div>
```

## 3 blog实现

之前写过一次博客了，这次打算功能齐全一点。每篇blog有一个分区，多个Tag。博客主页有列表、分类、标签、搜索等功能，

### 3.1 创建应用

用终端创建一个应用。

```
$ ./manage.py startapp blog
```

配置setting.py。

```python
INSTALLED_APPS = (
    ...
    'blog',
)

...

# 设置语言
LANGUAGE_CODE = 'en-us' # zh-hans
# 时区
TIME_ZONE = 'Asia/Shanghai'
```

### 3.2 Models模型构建

Post模型

- title
- author
- publish_date
- modify_date
- content
- category
- Tags

```python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(u"title", max_length=128)


class Tag(models.Model):
    title = models.CharField(u"title", max_length=128)
    
    
class Post(models.Model):
    title = models.CharField(u"title", max_length=128)
    author = models.ForeignKey(User)
    publish_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    content = models.TextField(u"content")
    category = models.ForeignKey(Category, verbose_name='title')
    tags = models.ManyToManyField(Tag, blank=False, null=False)

    class Meta:
        ordering = ["-id"]

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'post', (), {'pk': self.pk}
```

涉及到几个知识：

- DateTimeField的属性，auto_now_add 模型添加时的时间，auto_now 最后一次更新的时间
- ManyToManyField 多对多关系，还没试过。
- get_absolute_url 函数，方便求出模型对应的url。【那么问题来了，pk跟id的区别何在】

#### 网页登录admin观察

再设置admin管理的信息，

```python
from django.contrib import admin
...
class PostAdmin(admin.ModelAdmin):
    title = models.ForeignKey(Post, verbose_name='title')
    publish_date = models.ForeignKey(Post, verbose_name='publish_date')
    list_display = ('title', 'publish_date')
```

admin.py

```python
from django.contrib import admin
from .models import Post, PostAdmin
# Register your models here.

admin.site.register(Post, PostAdmin)
```

makemigrations, migrate

【tips】这个本来得在终端写，现在可以用Pycharm快速完成。详见 [http://blog.csdn.net/zhu_free/article/details/47776553](http://blog.csdn.net/zhu_free/article/details/47776553)

### 3.3 显示blog内容

要建立一个新的页面需要的三个步骤：

- urls.py里面添加一个网页链接，并指向到views里面的一个响应函数上
- views.py里面写一个函数进行相应，返回数据库内容以及templates里的一个html
- templates里面建立一个html文件，处理views.py传递进来的一些数据

我们在blog里面放一个urls.py，以 blog/ 开头的内容全都以这个urls里面的正则式重新开始匹配：

```python
# blog.urls
urlpatterns = [
    url(r'^$', 'blog.views.blog', name='blog'),
]
```

原本的website.urls中加上这样一句。

```python
    url(r'^blog/', include('blog.urls')),
```

blog.views中增加相应的函数

```python
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from blog.models import Post, Category

# Create your views here.


def blog(request):
    posts = Post.objects.all()

    ctx = {
        "posts": posts,
    }

    return render_to_response(
        'blog.html',
        ctx,
        context_instance=RequestContext(request)
    )
```

blog.html继承base.html的内容，处理views传递过来的ctx内容。

```html
{% extends "base.html" %}

{% block title %}Execution's Blogs{% endblock %}
{% block content %}


{% for post in posts %}
<div class="post">
	<h3><a href="{{ post.id }}" style="text-decoration:none;">{{ post.title }}</a></h3>
	<div class="info">
		<span class="category" style="color: #ff9900;">{{ post.category }}</span>
		<span class="author" style="color: #4a86e8">{{ post.author }}</span>
		<span class="pub_date" style="color: #6aa84f">{{ post.publication_date|date:"Y-m-d H:i" }}</span>
		<span class="mod_date" style="color: #000000"> | Updated: {{ post.modification_date|date:"Y-m-d H:i" }}</span>
	</div>
	<div class="summary">
		{{ post.content|slice:"64" }}...
	</div>
</div>
{% endfor %}

{% endblock %}

```

post.html也同理显示

## 3 功能性界面

### 3.1 markdown

[https://github.com/sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css)

使用这个样式，套一个标签\<article class="markdown-body"\>

一般性的用 {{ xx }} 传值会变成字符串，无法使用标签，所以要加上 {{ xx | safe }}

按照教程里面再搞个markup来提供markdown转码服务。坑：templatetags 必须重启 server 才能用。

python-markdown 提供的 sublist 要求 4spaces 的解决方案。[Nested lists require 4 spaces of indent](https://github.com/waylan/Python-Markdown/issues/3) 

### 3.2 upload file

正式发博之前，得实现图片上传功能。

[https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html](https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html)

我所期待的功能是，可以把它存到指定位置，还可以修改名称。

```python
def blog_upload(request, blog_pk):
    if request.method == 'POST' and request.FILES['image']:
        print 'ddd'
        file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save('static/img/post/%03d-%s' % (int(blog_pk), file.name), file)
        uploaded_url = fs.url(filename)
        return HttpResponse('Image upload success at ' + uploaded_url)

    return HttpResponse('File upload failed.')
```

做好上传功能后，html 表单 input[type="file"] 还是太丑，修改一下css吧。

## 4 远程部署

```
ps -ef
```

这条bash 指令查看所有 bg process

```
nohup ./manage.py runserver 0.0.0.0:80 &
```

迁徙的方法是git clone 之后 git pull，非常方便。