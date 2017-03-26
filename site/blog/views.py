from django.shortcuts import render
from . forms import PostForm, ParagraphForm, ImageForm
from functools import namedtuple
import re

def show_main_page(request):
	return render(request, 'blog/main_page.html')

def create_post(request):
	"""
	This view combine images and text sections of
	blog post and post name into a post.
	"""
	BlogSectionMeta = namedtuple('BlogSectionMeta', ['order',
													 'type'])	
	def parse_order(name):
		pattern = re.compile(r"(?P<order>\d+)-[\w]+")
		match = pattern.match(name)

		assert match is not None, \
			   '"{name}" is not correct'.format(name = name)

		return match.group("order")

	paragraphs_meta = []
	images_meta = []

	names = list(request.POST.keys()) + list(request.FILES.keys())
	for name in names:
		if 'paragraph' in name:
			order = parse_order(name)
			paragraphs_meta.append(BlogSectionMeta(order,
												   'paragraph'))
		elif 'image' in name:
			order = parse_order(name)
			images_meta.append(BlogSectionMeta(order,
										  	   'image'))

	sections_meta = paragraphs_meta + images_meta
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

	if all([f.is_valid() for f in forms]) and post_form.is_valid():
		post = post_form.save()
		for order, form in enumerate(forms):
			item = form.save(commit = False)
			item.post = post
			item.order = order
			item.save()
		return render(request, 'blog/main_page.html')
	else:
		return render(request,
					 'blog/create_post.html',
					 {
					 	'post_form': post_form,
					 	'forms': forms,
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