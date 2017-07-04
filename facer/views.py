from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage

from models import Photo

# Create your views here.


def facer_home(request):

	if request.method == 'POST' and request.FILES['upload_image']:
		file = request.FILES['upload_image']
		fs = FileSystemStorage()
		new_photo = Photo.objects.create()
		filename = 'static/img/facer/%06d-input.png' % int(new_photo.pk)
		if fs.exists(filename):
			fs.delete(filename)
		fs.save(filename, file)
		return HttpResponseRedirect('input/'+str(new_photo.pk))

	else:
		return render_to_response("facer_home.html", context_instance=RequestContext(request))


def facer_input(request, pk):

	img_src = '/static/img/facer/%06d-input.png' % int(pk)

	ctx = {
		'img_src': img_src
	}

	return render_to_response(
		"facer_input.html",
		ctx,
		context_instance=RequestContext(request)
	)