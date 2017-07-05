from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from website.settings import BASE_DIR
from models import Photo

import cv2
import os

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

		# Create the haar cascade
		cascPath = os.path.join(BASE_DIR, 'static/facer/haarcascade_frontalface_default.xml')
		faceCascade = cv2.CascadeClassifier(cascPath)

		# Read the image
		imagePath = os.path.join(BASE_DIR, filename)
		image = cv2.imread(imagePath)

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# Detect faces in the image
		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.2,
			minNeighbors=5,
			minSize=(30, 30)
		)

		for (x, y, w, h) in faces:
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
		cv2.imwrite(imagePath, image)

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