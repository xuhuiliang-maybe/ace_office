# coding=utf-8
from django.conf.urls import url

from modules.finance.arrival_and_billing.code.add_arrival_and_billing import *
from modules.finance.arrival_and_billing.code.del_arrival_and_billing import *
from modules.finance.arrival_and_billing.code.edit_arrival_and_billing import *
from modules.finance.arrival_and_billing.code.export_arrival_and_billing import *
from modules.finance.arrival_and_billing.code.list_arrival_and_billing import *

# 财务-到账与开票
urlpatterns = [
	url(r'^add$', ArrivalAndBillingCreate.as_view(), name="add_arrivalandbilling"),  # 增
	url(r'^(?P<pk>[0-9]+)/delete$', ArrivalAndBillingDelete.as_view(), name="del_arrivalandbilling"),  # 删
	url(r'^list$', ArrivalAndBillingListView.as_view(), name="list_arrivalandbilling"),  # 查
	url(r'^(?P<pk>[0-9]+)/edit$', ArrivalAndBillingUpdate.as_view(), name="edit_arrivalandbilling"),  # 改
	url(r'^export$', ArrivalAndBillingExportView.as_view(), name="export_arrivalandbilling"),  # 导出

	# 到账明细
	url(r'^(?P<arrivalandbilling>[0-9]+)/add_credited_details$', CreditedDetailsCreate.as_view(), name="add_crediteddetails"),  # 增
	# 删
	url(r'^(?P<arrivalandbilling>[0-9]+)/(?P<pk>[0-9]+)/delete_credited_details$', CreditedDetailsDelete.as_view(), name="del_crediteddetails"),
	url(r'^(?P<arrivalandbilling>[0-9]+)/list_credited_details$', CreditedDetailsListView.as_view(), name="list_crediteddetails"),  # 查
	# 改
	url(r'^(?P<arrivalandbilling>[0-9]+)/(?P<pk>[0-9]+)/edit_credited_details$', CreditedDetailsUpdate.as_view(), name="edit_crediteddetails"),

	# 开票明细
	url(r'^(?P<arrivalandbilling>[0-9]+)/add_billing_details$', BillingDetailsCreate.as_view(), name="add_billingdetails"),  # 增
	# 删
	url(r'^(?P<arrivalandbilling>[0-9]+)/(?P<pk>[0-9]+)/delete_billing_details$', BillingDetailsDelete.as_view(), name="del_billingdetails"),
	url(r'^(?P<arrivalandbilling>[0-9]+)/list_billing_details$', BillingDetailsListView.as_view(), name="list_billingdetails"),  # 查
	# 改
	url(r'^(?P<arrivalandbilling>[0-9]+)/(?P<pk>[0-9]+)/edit_billing_details$', BillingDetailsUpdate.as_view(), name="edit_billingdetails"),

]
