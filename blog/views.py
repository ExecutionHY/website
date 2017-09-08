from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from blog.models import Post, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.files.storage import FileSystemStorage

# Create your views here.

options = [{"num": 0, "info": "Public Time", "sys": "-publication_date"},
           {"num": 1, "info": "Modify Time", "sys": "-modification_date"},
           ]


def blog_home(request):
	page = request.GET.get('page', 1)
	option = request.GET.get('option', 1)
	if not option:
		option = 0
	else:
		option = int(option)
	post_list = Post.objects.all().order_by(options[option].get('sys'))

	paginator = Paginator(post_list, 2)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	ctx = {
		"posts": posts,
		"option": option,
		"options": options,
	}

	return render_to_response(
		'blog_home.html',
		ctx,
		context_instance=RequestContext(request)
	)


def blog_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	tags = post.tags.all()

	ctx = {
		"post": post,
		"tags": tags
	}

	return render_to_response(
		'blog_post.html',
		ctx,
		context_instance=RequestContext(request)
	)


def blog_category(request, pk):
	category = get_object_or_404(Category, pk=pk)
	categories = Category.objects.all()

	post_list = category.post_set.all()

	# pagination part
	page = request.GET.get('page', 1)
	paginator = Paginator(post_list, 10)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	ctx = {
		"categories": categories,
		"category": category,
		"posts": posts
	}

	return render_to_response(
		'blog_home.html',
		ctx,
		context_instance=RequestContext(request)
	)


def blog_search(request):

	request.encoding = 'utf-8'
	if 'q' in request.GET:
		keyword = request.GET['q'].encode('utf-8').lower()

		# check keyword in title & content
		posts = Post.objects.all()
		result = []
		for p in posts:
			if keyword in p.title.lower():
				result.append(p)
			else:
				if keyword in p.content.lower():
					result.append(p)
	else:
		result = None
		keyword = None

	# pagination part
	page = request.GET.get('page', 1)
	paginator = Paginator(result, 10)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	ctx = {
		"is_search": True,
		"keyword": keyword,
		"posts": posts,
	}

	return render_to_response(
		'blog_home.html',
		ctx,
		context_instance=RequestContext(request)
	)


# upload files, overwrite
def blog_upload(request, post_pk):

	if request.method == 'POST' and request.FILES['upload_image']:
		file = request.FILES['upload_image']
		fs = FileSystemStorage()
		filename = 'static/img/post/%03d-%s' % (int(post_pk), file.name)
		if fs.exists(filename):
			fs.delete(filename)
		fs.save(filename, file)
		uploaded_url = fs.url(filename)
		return HttpResponse('File upload success at ' + uploaded_url)

	return HttpResponse('File upload failed.')
