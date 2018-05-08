# coding=utf-8
from django.conf.urls import url

from modules.mysite.code import emails_views
from modules.mysite.code import personal_views
from modules.mysite.code import timelines_views

# 我的地盘
urlpatterns = [
	url(r'^personal$', personal_views.PersonalListView.as_view(), name='personal'),  # 列表，用户信息
	url(r'^personal/edit$', personal_views.PersonalUpdateView.as_view(), name='personal_edit'),  # 编辑，用户信息
	url(r'^emails$', emails_views.emails_list, name='emails'),
	url(r'^timelines$', timelines_views.time_lines, name='timelines'),
]
