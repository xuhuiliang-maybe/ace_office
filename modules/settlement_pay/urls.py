# coding=utf-8
from django.conf.urls import url

from modules.settlement_pay.code import payroll_add
from modules.settlement_pay.code import payroll_del
from modules.settlement_pay.code import payroll_edit
from modules.settlement_pay.code import payroll_list
from modules.settlement_pay.models import Payroll

# 结算发薪
urlpatterns = [
	url(r'^list$', payroll_list.PayrollListView.as_view(), name="payroll_list"),
	url(r'^add$', payroll_add.PayrollCreate.as_view(), name="payroll_add"),
	url(r'^(?P<pk>[0-9]+)/del$', payroll_del.PayrollDelete.as_view(), {"model_name": Payroll}, name="payroll_del"),
	url(r'^batchdelete$', payroll_del.PayrollBatchDelete.as_view(), name="payroll_batch_delete"),  # 批量删除
	url(r'^(?P<pk>[0-9]+)/edit$', payroll_edit.PayrollUpdate.as_view(), {"model_name": Payroll},
	    name="payroll_edit"),
]
