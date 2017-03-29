from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from . forms import PostForm, ParagraphForm, ImageForm
from functools import namedtuple
import re

def show_main_page(request):
	return render(request, 'blog/main_page.html')

# This class should help to work with models, which could
# have uncertained number of unordered fields
# Help to collect them, render with js/html
# class MixedForm:
# 	Meta = namedtuple('Meta', ['order', 'type'])
# 	def parse_order_name():
# 		pattern = re.compile(r'(?P<order>\d+)-(?P<type>\w+)')
# 		match = patter.match(name)
# 		return match.group('order'), match.group('type')

# 	def __init__(self, constructors):
# 		self.constructors = dict(zip(self.types, self.constructors))
# 		self.types = [type(constructor) for constructor in constructors]
# 	def combine_forms(request):
# 		names = list(request.POST.keys()) + list(request.FILES.keys())
# 		metas = []
# 		for name in names:
# 			if any([type in name for type in self.types]):
# 				order, type = parse_order_type(name)
# 				metas.append(Meta(order, type))
# 		metas.sort(key = lambda m: int(m.order))

# 		forms = [self.constructors[meta.type](request.POST or None, request.FILES or None, prefix = meta.order) for meta in metas]
# 		return forms
# 	def render(self, request):
# 		forms = combine_forms(request)
# 		[form.is_valid() for form in forms]
# 		return forms
def show_post(request, pk):
	"""
	This view retriews post for a certain pk
	and shows it.
	"""
	post = get_object_or_404(Post, pk = pk)
	post_sections_forms = list(post.images.all()) + list(post.paragraphs.all())
	post_sections_forms.sort(key = lambda field: field.order)
	return render(request,
				  'blog/show_post.html',
				  {'post': post,
				   'post_sections_forms': post_sections_forms})

def create_post(request):
	"""
	This view combine images and text sections of
	blog post and post name into a post.
	"""
	BlogSectionMeta = namedtuple('BlogSectionMeta', ['order',
													 'type'])

	def parse_order_and_type(name):
		pattern = re.compile(r"(?P<order>\d+)-(?P<type>\w+)")
		match = pattern.match(name)

		assert match is not None, \
			   '"{name}" is not correct'.format(name = name)

		return match.group('order'), match.group('type')

	# All names used in page
	fields_names = list(request.POST.keys()) + list(request.FILES.keys())

	# Names of fields that are blog sections
	sections_types = ('image', 'paragraph')

	# Meta about sections in page
	sections_meta = []

	# Check each field from request
	for field_name in fields_names:
		# Check whether field in list of blog section fields
		if any(section_type in field_name for section_type in sections_types):
			order, section_type = parse_order_and_type(field_name)
			sections_meta.append(BlogSectionMeta(order,
												 section_type))

	sections_meta.sort(key = lambda section: int(section.order))

	forms = []
	for section in sections_meta:
		if section.type == 'image':
			form = ImageForm(request.POST,
							 request.FILES,
							 prefix = section.order)
			forms.append(form)
		elif section.type == 'paragraph':
			form = ParagraphForm(request.POST,
								 prefix = section.order)
			forms.append(form)

	post_form = PostForm(request.POST or None, prefix = 'post')

	if all(f.is_valid() for f in forms) and post_form.is_valid():
		post = post_form.save()
		for order, form in enumerate(forms):
			item = form.save(commit = False)
			item.post = post
			item.order = order
			item.save()
		return redirect('show_post', pk = post.pk)
		# return render(request, 'blog/main_page.html')
	else:
		fields_counter = request.POST.get('fields_counter', 0)
		return render(request,
					 'blog/create_post.html',
					 {
					 	'post_form': post_form,
					 	'forms': forms,
					 	'fields_counter': fields_counter,
					 })



	# post_sections = paragraphs + images
	# post_sections = sorted(post_sections,
	# 					   key = lambda s:
	# 					   		   parse_order(list(s.keys())[0]))
	# for i, s in enumerate(post_sections):
	# 	key = list(s.keys())[0]
	# 	new_key = re.sub(r'-\d+', '', key)
	# 	post_sections[i][new_key] = post_sections[i].pop(key)

	# forms = [ImageForm({}, s) if 'image' in list(s.keys())[0]
	# 					  else ParagraphForm(s)
	# 					  for s in post_sections]

	# if all([form.is_valid() for form in forms]) and post_form.is_valid():
	# 	post = post_form.save()
	# 	for i, form in enumerate(forms):
	# 		item = form.save(commit = False)
	# 		item.order = i
	# 		item.post = post
	# 		item.save()
	# 	return render(request, 'blog/main_page.html')

	# return render(
	# 	request,
	# 	'blog/create_post.html',
	# 	{
	# 		'post_form': post_form,
	# 		'forms': forms,
	# 	}
	# )
	# post_form = PostForm(request.POST or None, prefix = 'post')
	
	# paragraphs = []
	# for key, value in request.POST.items():
	# 	if 'paragraph' in key:
	# 		paragraphs.append({key: value})

	# images = []
	# for key, value in request.FILES.items():
	# 	if 'image' in key:
	# 		images.append({key: value})

	# def parse_order(s):
	# 	pattern = re.compile(r"[\w-]*-(?P<order>\d+)")
	# 	match = pattern.match(s)
	# 	return int(match.group("order"))

	# post_sections = paragraphs + images
	# post_sections = sorted(post_sections,
	# 					   key = lambda s:
	# 					   		   parse_order(list(s.keys())[0]))
	# for i, s in enumerate(post_sections):
	# 	key = list(s.keys())[0]
	# 	new_key = re.sub(r'-\d+', '', key)
	# 	post_sections[i][new_key] = post_sections[i].pop(key)

	# forms = [ImageForm({}, s) if 'image' in list(s.keys())[0]
	# 					  else ParagraphForm(s)
	# 					  for s in post_sections]

	# if all([form.is_valid() for form in forms]) and post_form.is_valid():
	# 	post = post_form.save()
	# 	for i, form in enumerate(forms):
	# 		item = form.save(commit = False)
	# 		item.order = i
	# 		item.post = post
	# 		item.save()
	# 	return render(request, 'blog/main_page.html')

	# return render(
	# 	request,
	# 	'blog/create_post.html',
	# 	{
	# 		'post_form': post_form,
	# 		'forms': forms,
	# 	}
	# )