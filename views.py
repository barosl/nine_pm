from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from models import *

def index(req):
	return render_to_response('index.html', RequestContext(req, {
		'form': AuthenticationForm(),
		'next': req.GET['next'] if 'next' in req.GET else reverse(intro),
	}))

@login_required
def intro(req):
	return render_to_response('intro.html', RequestContext(req))

@login_required
def forums(req):
	mins = sum(x.mins for x in UserStay.objects.filter(user=req.user))

	return render_to_response('forums.html', RequestContext(req, {
		'hours': mins/60,
		'mins': mins%60,
		'forums': Forum.objects.all(),
	}))

@login_required
def forum(req, forum_id):
	forum = get_object_or_404(Forum, pk=forum_id)

	return render_to_response('forum.html', RequestContext(req, {
		'forum': forum,
		'posts': Post.objects.filter(forum=forum),
	}))

@login_required
def post(req, post_id):
	return render_to_response('post.html', RequestContext(req, {
	}))
