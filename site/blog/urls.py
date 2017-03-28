from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.show_main_page, name = 'show_main_page'),
	url(r'^new$', views.create_post, name = 'create_post'),
	url(r'^show/(?P<pk>\d+)', views.show_post, name = 'show_post'),
]