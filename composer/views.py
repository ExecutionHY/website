# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


def composer_home(request):

    return render_to_response("composer_home.html", context_instance=RequestContext(request))
