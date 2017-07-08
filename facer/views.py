from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from website.settings import BASE_DIR
from models import Photo

import cv2
import os

# Create your views here.


def facer_home(request):

	return render_to_response("facer_home.html", context_instance=RequestContext(request))


def facer1_input(request):

	if request.method == 'POST' and request.FILES['upload_image']:
		file = request.FILES['upload_image']
		fs = FileSystemStorage()
		new_photo = Photo.objects.create()
		filename = 'static/img/facer1/%06d-input.png' % int(new_photo.pk)
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

		faces = sorted(faces, key=lambda face: face[0])
		cnt = 0
		for (x, y, w, h) in faces:
			cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 255), 2)
			cv2.putText(image, str(cnt), (x+w/2, y+int(h*1.5)), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
			cnt += 1

		cv2.imwrite(imagePath, image)

		ctx = {
			'img_src': '/'+filename,
			'img_pk': new_photo.pk,
			'count_list': [x for x in range(0, len(faces))],
		}

		return render_to_response(
			"facer_input.html",
			ctx,
			context_instance=RequestContext(request)
		)

	ctx = {
		'img_src': '/static/img/facer1/000000-input.png'
	}

	return render_to_response(
		"facer_input.html",
		ctx,
		context_instance=RequestContext(request)
	)