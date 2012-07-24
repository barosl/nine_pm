from django import forms
from models import *

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude = ['user', 'ctime', 'mtime', 'points']
		widgets = {
			'forum': forms.HiddenInput,
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		exclude = ['user', 'ctime', 'mtime']
		widgets = {
			'post': forms.HiddenInput,
		}

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		exclude = ['user']
