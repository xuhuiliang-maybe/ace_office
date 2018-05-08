# coding=utf-8
from django.conf.urls import url

from modules.payroll_manage.payroll_detail.code import (
	payroll_detail_views,
	payroll_detail_add_views,
	payroll_detail_edit_views,
	payroll_detail_delete
)
from modules.payroll_manage.payroll_detail.models import PayrollDetail

# 薪资明细
urlpatterns = [
	url(r'^list$', payroll_detail_views.PayrollDetailListView.as_view(), name="payroll_detail_list"),
	url(r'^payroll_detail_add$', payroll_detail_add_views.PayrollDetailCreate.as_view(), name="payroll_detail_add"),
	url(r'^payroll_detail_(?P<pk>[0-9]+)/edit$', payroll_detail_edit_views.PayrollDetailUpdate.as_view(),
	    {"model_name": PayrollDetail}, name="payroll_detail_edit"),
	url(r'^payroll_detail_(?P<pk>[0-9]+)/delete$', payroll_detail_delete.PayrollDetailDelete.as_view(),
	    {"model_name": PayrollDetail}, name="payroll_detail_delete"),
]
