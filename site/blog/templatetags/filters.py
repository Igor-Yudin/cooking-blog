from django.contrib.staticfiles.templatetags.staticfiles import static
from django import template

register = template.Library()

@register.filter(name = 'get_item')
def get_item(dictionary, key):
	return dictionary.get(key)

@register.filter(name = 'get_image_url')
def get_image_url(image_name):
	"""
	Returns string url(image_path).
	"""
	if image_name == None:
		return 'none'
	return "url(%s)" % static('images/' + image_name)

@register.filter(name = 'linebreaksp')
def linebreaksp(text):
	"""
	Returns text with all new lines turned into p.
	"""
	text = text.split('\n')
	return "".join(["<p>%s</p>" % block for block in text])

@register.filter(name = 'get_model_name')
def get_class_name(obj):
	"""
	Returns object model name.
	"""
	return obj.__class__.__name__