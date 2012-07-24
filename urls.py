from django.conf.urls import patterns, include, url
from views import *
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('',
	url(r'^$', index),
	url(r'^login/$', login, {'template_name': 'index.html'}),
	url(r'^logout/$', logout, {'next_page': reverse_lazy(index)}),
	url(r'^intro/$', intro),
	url(r'^forums/$', forums),
	url(r'^forum/(\d+)/$', forum),
	url(r'^post/(\d+)/$', post),
)
