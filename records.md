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

#### html css

[https://github.com/sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css)

使用这个样式，套一个标签\<article class="markdown-body"\>

一般性的用 {{ xx }} 传值会变成字符串，无法使用标签，所以要加上 {{ xx | safe }}

#### markdown to html

按照教程里面再搞个markup来提供markdown转码服务。坑：templatetags 必须重启 server 才能用。

python-markdown 提供的 sublist 要求 4spaces 的解决方案。[Nested lists require 4 spaces of indent](https://github.com/waylan/Python-Markdown/issues/3) 

#### code highlight

highlight这次怎么实现好呢。[http://peter-hoffmann.com/2012/python-markdown-github-flavored-code-blocks.html ](http://peter-hoffmann.com/2012/python-markdown-github-flavored-code-blocks.html)看了这篇博客，我决定使用js来搞。它有一点好，就是还可以拓展语言，之前 python-markdown 的高亮拓展中 bash 就是没有的。

关于配色主题，他也给出了许多方案，我选择了 github-gist 主题，还不错。

#### line-numbering

一开始我希望用插件实现，后来发现跟高亮插件的兼容性等都存在问题。后来在网上找了一个 js 代码，直接统计 code 的行数然后显示。

```javascript
//numbering for pre>code blocks
$(function(){
    $('pre code').each(function(){
        var lines = $(this).text().split('\n').length - 1;
        var $numbering = $('<div/>').addClass('pre-numbering');
        $(this).addClass('has-numbering');
        $(this).parent().prepend($numbering);

        var str = "";
        for(i = 1;i <= lines; i++){
            str += i+"\n"
        }
        $numbering.html(str);
    });
});
```

我们用 css 属性 float 来实现两列并排，再加上一点 padding。

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

### 3.3 override admin

我们的需求是，重载 admin 页面，把 upload 的按钮给放上去。重载的方法根据文档所述。

[https://docs.djangoproject.com/en/dev/ref/contrib/admin/#adminsite-objects](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#adminsite-objects)

简单归纳，就是把一个同名 html 放到 templates/admin/app_name/ 目录下，它在查找这个 html 时会优先从这里取。同时我们把原版 html 放在 templates/admin/ 下，再用这个新的去继承它。

[https://raw.githubusercontent.com/django/django/1.8.1/django/contrib/admin/templates/admin/change_form.html](https://raw.githubusercontent.com/django/django/1.8.1/django/contrib/admin/templates/admin/change_form.html)

例如我继承了这个页面。而我新的 change_form.html 页面这样写：

```html
{% extends "admin/change_form.html" %}
{% block after_related_objects %}
	<form method="post" enctype="multipart/form-data" action="upload/">
      {% csrf_token %}
      <input type="file" name="image">
      <button type="submit">Upload Image</button>
  </form>
{% endblock %}
```

### 3.4 Disqus Comment

跟多说什么的原理差不多啦。不过一开始给你提供的代码得改改，需要设置好config部分。

一开始我遇到的问题是，多个页面显示同一个评论。根据官方的介绍，你必须保证 url 和 identifier 都是 unique 的。真的奇怪的是 url 的设置，我现在莫名地加一段 #comment 上去，如果不加的话，最后的 pk 这个数字不会被传到 thread 上，就会导致不 unique，是了很多遍，最后就决定这么写了。

```html
<div id="disqus_thread">You may not be able to access <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></div>
<script>

/**
*  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
*  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables*/

var disqus_config = function () {
	this.page.url = 'http://www.execution.website/blog/post/{{ post.pk }}#comment';  // Replace PAGE_URL with your page's canonical URL variable
	this.page.identifier = 'blog-{{ post.pk }}'; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
};

(function() { // DON'T EDIT BELOW THIS LINE
	var d = document, s = d.createElement('script');
	s.src = 'https://execution-1.disqus.com/embed.js';
	s.setAttribute('data-timestamp', +new Date());
	(d.head || d.body).appendChild(s);
})();
</script>
```

### 3.5 pagination 分页

TUTORIAL [https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html](https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html)

css [https://www.w3schools.com/css/css3_pagination.asp](https://www.w3schools.com/css/css3_pagination.asp)

## 4 远程部署

这条 bash 指令查看所有 bg process

```shell
ps -ef
```

这条指令让服务器无限后台运行

```shell
nohup ./manage.py runserver 0.0.0.0:80 &
```

在这个文件中加入shell 代码来开机运行。

```
/etc/rc.local
```

迁徙的方法是git clone 之后 git pull，非常方便。

### DEBUG

发布自己的网站后记得把 setting.py 的 DEBUG 设置为 False。同时要设置好 ALLOWED_HOSTS（其实可以用 \* 正则表示

```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "23.83.232.175", "www.execution.website"]
```

### STATIC

```python
### settings.py
STATIC_URL = '/static/'

# used in DEBUG=True
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static').replace('\\', '/'),
)

# used in DEBUG=False
STATIC_ROOT = (
    os.path.join(BASE_DIR, 'static')
)

### urls.py
url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': STATIC_ROOT}),
```

我们本来是不搞这些花样的，在 DEBUG = True 的时候只要依靠 settings 的前两个设置就够了。但是 DEBUG = False 不允许我们对 static 进行 serve，这就很糟糕了，所以我们建立两个设置，当 False 时搞一个自己的 document serve，地址就还是这个地址，但是你必须保证两个 static 地址是不同的，因此我们把其中一个给改一下形式。

### CDN

因为我这个服务器很慢，带宽有限，利用 CDN 可以减少用户请求的数据量。 [http://www.bootcdn.cn/](http://www.bootcdn.cn/) 尽量用国内的 CDN，经我测试，国外的 cdn 例如 [https://www.cloudflare.com/](https://www.cloudflare.com/) 的，还没我自己的服务器快。

### 如何让自己的网站被 Google 检索到

http://www.steegle.com/websites/google-sites-howtos/get-found-google-search#TOC-Set-your-Site-s-Visibility

## 5 App Develop Log

### Facer 1.0

### Puncher

- 0.1 # database design
- 0.2 # colorblock display
- 0.3 # data filter by date
- 0.4 # slider design
- 0.5 # slider design / mouse&touch
- 0.6 # payment model
- 1.0 # payment puncher
- 1.1 # monthly data bar
- 1.2 # execution's bill
- 1.3 # add checkpoint interface
- 1.4 # todo list slider response
- 1.5 # money data instruction
- 1.5.1 # update homepage




## 6 Javascript Tips

### Post

发送数据到后端，Django 提供了一个 form 的模板，还算中规中矩，只是自由度感觉不高，因此要研究一下 js (Jquery/ajax) 的 post 交互方案。

一开始以为用 ajax 的 post 可以很简单，结果 403，后来发现 form 在提交的时候必须携带 csrf 的值，于是乎我就直接把这个值给扒来了。（这个值的来源是后面其他 form 中的 {% csrf_token %} 标签）

```javascript
function punch() {
    var task = obj_.id[4];
    var csrftoken = document.getElementsByName("csrfmiddlewaretoken").item(0).value;
    $.post('', {'taskNo': task, 'csrfmiddlewaretoken': csrftoken });
}
```

