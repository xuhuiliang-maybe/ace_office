# coding=utf-8
from django.conf.urls import url

from modules.payroll_manage.payroll_gather.code import payroll_gather_views

# 薪资汇总
urlpatterns = [
	url(r'^list$', payroll_gather_views.PayrollGatherListView.as_view(), name="payroll_gather_list"),
]
