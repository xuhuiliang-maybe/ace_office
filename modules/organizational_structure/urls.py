# coding=utf-8
from django.conf.urls import include, url

from modules.organizational_structure.structures.code import structure_views

# 组织架构
urlpatterns = [
	# 组织架构图
	url(r'^structure$', structure_views.StructureListView.as_view(), name="structure"),

	# 部门信息
	url(r'^departments/', include('modules.organizational_structure.departments.urls', namespace="departments")),

	# 用户信息
	url(r'^profile/', include('modules.organizational_structure.profiles.urls', namespace='profile')),
]
