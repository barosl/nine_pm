from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from models import *
from datetime import datetime
from forms import *

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

	form = PostForm(initial={'forum': forum})

	return render_to_response('forum.html', RequestContext(req, {
		'forum': forum,
		'posts': Post.objects.filter(forum=forum).order_by('-ctime'),
		'form': form,
	}))

@login_required
def post_new(req):
	post = PostForm(req.POST).save(commit=False)
	post.user = req.user
	post.ctime = post.mtime = datetime.now()
	post.points = 0
	post.save()

	return redirect(globals()['post'], post.pk)

@login_required
def post(req, post_id):
	post = get_object_or_404(Post, pk=post_id)

	form = CommentForm(initial={'post': post})

	return render_to_response('post.html', RequestContext(req, {
		'post': post,
		'comments': Comment.objects.filter(post=post).order_by('-ctime'),
		'form': form,
	}))

def comment_new(req):
	comment = CommentForm(req.POST).save(commit=False)
	comment.user = req.user
	comment.ctime = comment.mtime = datetime.now()
	comment.save()

	return redirect(globals()['post'], comment.post.pk)
