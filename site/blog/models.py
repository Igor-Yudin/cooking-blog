from django.db import models

class Post(models.Model):
	name = models.CharField(max_length = 255)
	date = models.DateField(auto_now_add = True)
	slug = models.SlugField(max_length = 255, blank = True)

	def publish(self):
		pass

	def __str__(self):
		return self.name

class Paragraph(models.Model):
	paragraph = models.TextField()
	post = models.ForeignKey(
		Post,
		on_delete = models.CASCADE,
		related_name = 'paragraphs',
		blank = True
	)
	order = models.IntegerField(blank = True)

# Should use custom file storage system in order not
# to save all images locally
class Image(models.Model):
	image = models.ImageField(upload_to = 'images')
	post = models.ForeignKey(
		Post,
		on_delete = models.CASCADE,
		related_name = 'images',
		blank = True
	)
	order = models.IntegerField(blank = True)