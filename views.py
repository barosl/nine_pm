from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from models import *
from datetime import datetime
from forms import *
from django.http import HttpResponse
import time
from django.contrib.auth import login

def index(req):
	posts = [Post.objects.filter(forum=forum).order_by('-points')[0] for forum in Forum.objects.all()]

	return render_to_response('index.html', RequestContext(req, {
		'form': AuthenticationForm(),
		'next': req.GET['next'] if 'next' in req.GET else reverse(intro),
		'posts': posts,
	}))

@login_required
def intro(req):
	return render_to_response('intro.html', RequestContext(req))

@login_required
def forums(req):
	secs = sum(x.secs for x in UserStay.objects.filter(user=req.user))

	return render_to_response('forums.html', RequestContext(req, {
		'hours': secs//3600,
		'mins': secs%3600//60,
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
		'flowers': xrange(post.points),
	}))

@login_required
def comment_new(req):
	comment = CommentForm(req.POST).save(commit=False)
	comment.user = req.user
	comment.ctime = comment.mtime = datetime.now()
	comment.save()

	return redirect(globals()['post'], comment.post.pk)

@login_required
def post_vote(req, post_id):
	post = get_object_or_404(Post, pk=post_id)

	try: user_stay = UserStay.objects.get(user=req.user, forum=post.forum)
	except UserStay.DoesNotExist: user_stay = UserStay(user=req.user, forum=post.forum, secs=0)

	if req.POST.get('mode'):
		if user_stay.secs < post.forum.xch_rate*60:
			return HttpResponse('Insufficient points.') # FIXME: more friendly error message needed

		user_stay.secs -= post.forum.xch_rate*60
		user_stay.save()

		post.points = post.points + 1 # FIXME: may cause data inconsistency
		post.save()

		return redirect(globals()['post'], post.pk)
	else:
		return render_to_response('post_vote.html', RequestContext(req, {
			'post': post,
			'hours': user_stay.secs//3600,
			'mins': user_stay.secs%3600//60,
			'required_mins': post.forum.xch_rate,
		}))

@login_required
def user_stay(req, forum_id):
	forum = get_object_or_404(Forum, pk=forum_id)

	try: user_stay = UserStay.objects.get(user=req.user, forum=forum)
	except UserStay.DoesNotExist: user_stay = UserStay(user=req.user, forum=forum, secs=0)

	user_stay.secs += 5
	user_stay.last_seen = time.time()
	user_stay.save()

	return HttpResponse('/* nothing done here */', content_type='application/x-javascript')

def user_new(req):
	form = UserCreationForm(req.POST if req.POST else None)
	profile_form = UserProfileForm(req.POST if req.POST else None)

	if form.is_valid() and profile_form.is_valid():
		user = form.save(commit=False)
		user.is_staff = True
		user.is_superuser = True
		user.save()

		user_profile = profile_form.save(commit=False)
		user_profile.user = user
		user_profile.save()

		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(req, user)

		return redirect(index)

	return render_to_response('user_new.html', RequestContext(req, {
		'form': form,
		'profile_form': profile_form,
	}))
