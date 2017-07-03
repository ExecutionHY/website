from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from blog.models import Post, Category

from django.core.files.storage import FileSystemStorage

# Create your views here.


def blog_home(request):
	posts = Post.objects.all()

	ctx = {
		"posts": posts,
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

	posts = category.post_set.all()

	ctx = {
		"categories": categories,
		"category": category,
		"posts": posts
	}

	return render_to_response(
		'blog_display.html',
		ctx,
		context_instance=RequestContext(request)
	)


def blog_search(request):

	request.encoding = 'utf-8'
	if 'q' in request.GET:
		keyword = request.GET['q'].encode('utf-8').lower()

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

	ctx = {
		"is_search": True,
		"keyword": keyword,
		"posts": result,
	}

	return render_to_response(
		'blog_home.html',
		ctx,
		context_instance=RequestContext(request)
	)


def blog_upload(request, post_pk):
	if request.method == 'POST' and request.FILES['image']:
		print 'ddd'
		file = request.FILES['image']
		fs = FileSystemStorage()
		filename = 'static/img/post/%03d-%s' % (int(post_pk), file.name)
		if fs.exists(filename):
			fs.delete(filename)
		fs.save(filename, file)
		uploaded_url = fs.url(filename)
		return HttpResponse('File upload success at ' + uploaded_url)
	else:
		return HttpResponse('File upload failed.')
