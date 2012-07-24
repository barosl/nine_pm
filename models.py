from django.db import models
from django.contrib.auth.models import User

class Forum(models.Model):
	name = models.CharField(max_length=100)

	ex_rate = models.IntegerField()
	img = models.ImageField(upload_to='forums')

class Post(models.Model):
	forum = models.ForeignKey(Forum)
	user = models.ForeignKey(User)

	name = models.CharField(max_length=100)
	text = models.TextField()
	ctime = models.DateTimeField()
	mtime = models.DateTimeField()
	points = models.IntegerField()

class Comment(models.Model):
	post = models.ForeignKey(Post)
	user = models.ForeignKey(User)

	text = models.TextField()
	ctime = models.DateTimeField()
	mtime = models.DateTimeField()

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	name = models.CharField(max_length=100)

class UserPoints(models.Model):
	user = models.ForeignKey(User)
	forum = models.ForeignKey(Forum)
	mtime = models.IntegerField()
	points = models.IntegerField()
