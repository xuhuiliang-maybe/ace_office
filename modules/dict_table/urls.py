# coding=utf-8
from django.conf.urls import url

from modules.dict_table.code.dict_tables_views import *

# 字典表
urlpatterns = [
	url(r'^(?P<dict_table_type>\w+)$', DictTableList.as_view(), name="list"),
	url(r'^(?P<dict_table_type>\w+)/add$', DictTableAdd.as_view(), name="add"),
	url(r'^(?P<dict_table_type>\w+)/(?P<pk>[0-9]+)/edit$', DictTableEdit.as_view(), name="edit"),
	url(r'^(?P<dict_table_type>\w+)/(?P<pk>[0-9]+)/delete$', DictTableDel.as_view(), name="delete"),
]
