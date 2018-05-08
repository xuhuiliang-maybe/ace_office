# coding=utf-8
from django.conf.urls import url

from modules.home_page.code import homepage_views

# 网站主页
urlpatterns = [
	url(r'^index$', homepage_views.IndexView.as_view(), name='index'),
]
