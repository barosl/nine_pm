from django.db import models
from django.contrib.auth.models import User

class Forum(models.Model):
	name = models.CharField(max_length=100)

	xch_rate = models.IntegerField()
	img = models.ImageField(upload_to='forums')

	def __unicode__(self):
		return 'Forum named "%s"' % self.name

class Post(models.Model):
	forum = models.ForeignKey(Forum)
	user = models.ForeignKey(User)

	name = models.CharField(max_length=100)
	text = models.TextField()
	ctime = models.DateTimeField()
	mtime = models.DateTimeField()
	points = models.IntegerField()

	def __unicode__(self):
		return 'Post titled "%s"' % self.name

class Comment(models.Model):
	post = models.ForeignKey(Post)
	user = models.ForeignKey(User)

	text = models.TextField()
	ctime = models.DateTimeField()
	mtime = models.DateTimeField()

	def __unicode__(self):
		return 'Comment by "%s"' % self.user.username

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	name = models.CharField(max_length=100)

	def __unicode__(self):
		return 'User profile of "%s"' % self.user.username

class UserStay(models.Model):
	user = models.ForeignKey(User)
	forum = models.ForeignKey(Forum)

	last_seen = models.IntegerField()
	secs = models.IntegerField()

	def __unicode__(self):
		return 'User points of "%s"' % self.user.username
