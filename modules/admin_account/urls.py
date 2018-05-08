# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.views import password_change
from django.contrib.auth.views import password_change_done

from modules.admin_account.code import login_views

# 用户权限
urlpatterns = [
	url(r'^login/$', login_views.user_login, name='login'),
	url(r'^logout/$', login_views.user_logout, name='logout'),

	url(r'^password_change/$', password_change,
	    {"template_name": "password_change_form.html", "post_change_redirect": "/accounts/password_change/done/"},
	    name='password_change'),
	url(r'^password_change/done/$', password_change_done, {"template_name": "password_change_done.html"},
	    name='password_change_done'),

]
