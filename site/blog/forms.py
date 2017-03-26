from django import forms
from .models import Paragraph, Image, Post
from django.utils.translation import ugettext_lazy as _

class ParagraphForm(forms.ModelForm):
	class Meta:
		model = Paragraph
		exclude = ('order', 'post',)

class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		exclude = ('order', 'post',)

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude = ('slug',)