# coding=utf-8
from django.conf.urls import url

from modules.employee_management.employee_info.code import employee_views, employee_add_views, employee_delete, \
	employee_edit_views, load_employee_views, employee_export_views
from modules.employee_management.employee_info.models import Employee

urlpatterns = [
	# 员工信息
	url(r'^(?P<employee_type>\w+)/list$', employee_views.EmployeeList.as_view(), name="list"),  # 员工列表
	url(r'^add/employee$', employee_add_views.EmployeeCreate.as_view(), name="employee_add"),  # 新增
	url(r'^(?P<pk>[0-9]+)/edit/employee$', employee_edit_views.EmployeeUpdate.as_view(), {"model_name": Employee},
	    name="employee_edit"),  # 编辑
	url(r'^(?P<pk>[0-9]+)/delete/employee$', employee_delete.EmployeeDelete.as_view(), {"model_name": Employee},
	    name="employee_delete"),
	# 删除

	# 批量删除
	url(r'employee/batchdelete$', employee_delete.EmployeesBatchDelete.as_view(), name="employee_batch_delete"),

	# 导入
	url(r'^load/employee$', load_employee_views.LoadEmployeeView.as_view(), {"emp_type": "employee"},
	    name="employee_load"),
	# 导出
	url(r'^export$', employee_export_views.EmployeeExportView.as_view(), name="employee_export"),

	# 临时工信息
	url(r'^add/temporary$', employee_add_views.TemporaryCreate.as_view(), name="temporary_add"),  # 新增

	# 编辑
	url(r'^(?P<pk>[0-9]+)/edit/temporary$', employee_edit_views.TemporaryUpdate.as_view(), {"model_name": Employee},
	    name="temporary_edit"),

	# 删除
	url(r'^(?P<pk>[0-9]+)/delete/temporary$', employee_delete.TemporaryDelete.as_view(), {"model_name": Employee},
	    name="temporary_delete"),

	# 批量删除
	url(r'^temporary/batchdelete$', employee_delete.TemporaryBatchDelete.as_view(),
	    name="temporary_batchdelete_delete"),

	url(r'^load/temporary$', load_employee_views.LoadEmployeeView.as_view(), {"emp_type": "temporary"},
	    name="temporary_load"),  # 临时工导入
]
