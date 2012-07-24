from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm

def index(req):
	return render_to_response('index.html', RequestContext(req, {
		'form': AuthenticationForm()
	}))
