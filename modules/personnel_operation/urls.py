# coding=utf-8
from django.conf.urls import url

from modules.personnel_operation.code import personnel_add
from modules.personnel_operation.code import personnel_del
from modules.personnel_operation.code import personnel_edit
from modules.personnel_operation.code import personnel_list
from modules.personnel_operation.gather_code import gather_views
from modules.personnel_operation.models import QualityAssurance

# 人员操作质量
urlpatterns = [
	# 个人操作质量
	url(r'^list$', personnel_list.PersonnelList.as_view(), name="personnel_list"),
	url(r'^add$', personnel_add.PersonnelCreate.as_view(), name="personnel_add"),
	url(r'^(?P<pk>[0-9]+)/delete$', personnel_del.PersonnelDelete.as_view(), {"model_name": QualityAssurance},
	    name="personnel_del"),
	url(r'^(?P<pk>[0-9]+)/edit$', personnel_edit.PersonnelUpdate.as_view(), {"model_name": QualityAssurance},
	    name="personnel_edit"),

	# 操作质量
	url(r'^gather$', gather_views.GatherList.as_view(), name="gather_list"),
]
