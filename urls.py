from django.conf.urls import patterns, include, url
from views import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
	url(r'^$', index),
	url(r'^login/$', login, {'template_name': 'index.html'}),
	url(r'^logout/$', logout, {'next_page': '/'}),
)
