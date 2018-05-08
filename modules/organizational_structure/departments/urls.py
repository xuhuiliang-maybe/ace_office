# coding=utf-8
from django.conf.urls import url

from modules.organizational_structure.departments.code import (departments_views, add_department, del_department,
							       edit_departments)

# 部门信息
urlpatterns = [
	url(r'^list$', departments_views.DepartmentsListView.as_view(), name="departments_list"),  # 查询
	url(r'^add$', add_department.DepartmentsAdd.as_view(), name="departments_add"),  # 新增
	url(r'^(?P<pk>[\w]+)/edit$', edit_departments.DepartmentEdit.as_view(), name="departments_edit"),  # 编辑
	url(r'^del$', del_department.DepartmentsDelView.as_view(), name="departments_del"),  # 删除
]
