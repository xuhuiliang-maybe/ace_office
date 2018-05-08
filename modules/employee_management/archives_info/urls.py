# coding=utf-8
from django.conf.urls import url

from modules.employee_management.archives_info.code import del_archive
from modules.employee_management.archives_info.code import edit_archive
from modules.employee_management.archives_info.code import list_archive
from modules.employee_management.employee_info.models import Archive

# 档案信息相关
urlpatterns = [
	url(r'^list$', list_archive.ArchiveList.as_view(), name="archive_list"),
	url(r'^(?P<pk>[0-9]+)/edit$', edit_archive.ArchiveUpdate.as_view(), {"model_name": Archive},
	    name="archive_edit"),
	url(r'^(?P<pk>[0-9]+)/delete$', del_archive.ArchiveDelete.as_view(), {"model_name": Archive},
	    name="archive_delete")
]
