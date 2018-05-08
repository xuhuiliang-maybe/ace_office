# coding=utf-8
from django.conf.urls import url

from modules.contract_manage.hourly.add_hourly import ContractHourlyCreate
from modules.contract_manage.hourly.delete_hourly import ContractHourlyDelete
from modules.contract_manage.hourly.edit_hourly import ContractHourlyUpdate
from modules.contract_manage.hourly.list_hourly import ContractHourlyListView
from modules.contract_manage.intern.add_intern import ContractInternCreate
from modules.contract_manage.intern.delete_intern import ContractInternDelete
from modules.contract_manage.intern.edit_intsern import ContractInternUpdate
from modules.contract_manage.intern.list_intern import ContractInternListView
from modules.contract_manage.outsourc.add_outsourc import ContractOutsourcCreate
from modules.contract_manage.outsourc.delete_outsourc import ContractOutsourcDelete
from modules.contract_manage.outsourc.edit_outsourc import ContractOutsourcUpdate
from modules.contract_manage.outsourc.list_outsourc import ContractOutsourcListView
from modules.contract_manage.preview.download_contract import DownloadContractView
from modules.contract_manage.preview.generate_preview_code import *
from modules.contract_manage.preview.list_preview_code import *
from modules.contract_manage.send.add_send import ContractSendCreate
from modules.contract_manage.send.delete_send import ContractSendDelete
from modules.contract_manage.send.edit_send import ContractSendUpdate
from modules.contract_manage.send.list_send import ContractSendListView
from modules.contract_manage.service.add_service import ContractServiceCreate
from modules.contract_manage.service.delete_service import ContractServiceDelete
from modules.contract_manage.service.edit_service import ContractServiceUpdate
from modules.contract_manage.service.list_service import ContractServiceListView

urlpatterns = [
	# 合同签订-派遣
	url(r'^send$', ContractSendListView.as_view(), name="list_send"),
	url(r'^send/(?P<pk>[0-9]+)/delete$', ContractSendDelete.as_view(), name="delete_send"),
	url(r'^send/add$', ContractSendCreate.as_view(), name="add_send"),
	url(r'^send/(?P<pk>[0-9]+)/edit$', ContractSendUpdate.as_view(), name="edit_send"),

	# 合同签订-外包
	url(r'^outsourc$', ContractOutsourcListView.as_view(), name="list_outsourc"),
	url(r'^outsourc/(?P<pk>[0-9]+)/delete$', ContractOutsourcDelete.as_view(), name="delete_outsourc"),
	url(r'^outsourc/add$', ContractOutsourcCreate.as_view(), name="add_outsourc"),
	url(r'^outsourc/(?P<pk>[0-9]+)/edit$', ContractOutsourcUpdate.as_view(), name="edit_outsourc"),

	# 合同签订-实习生
	url(r'^intern$', ContractInternListView.as_view(), name="list_intern"),
	url(r'^intern/(?P<pk>[0-9]+)/delete$', ContractInternDelete.as_view(), name="delete_intern"),
	url(r'^intern/add$', ContractInternCreate.as_view(), name="add_intern"),
	url(r'^intern/(?P<pk>[0-9]+)/edit$', ContractInternUpdate.as_view(), name="edit_intern"),

	# 合同签订-劳务
	url(r'^service$', ContractServiceListView.as_view(), name="list_service"),
	url(r'^service/(?P<pk>[0-9]+)/delete$', ContractServiceDelete.as_view(), name="delete_service"),
	url(r'^service/add$', ContractServiceCreate.as_view(), name="add_service"),
	url(r'^service/(?P<pk>[0-9]+)/edit$', ContractServiceUpdate.as_view(), name="edit_service"),

	# 合同签订-小时工
	url(r'^hourly$', ContractHourlyListView.as_view(), name="list_hourly"),
	url(r'^hourly/(?P<pk>[0-9]+)/delete$', ContractHourlyDelete.as_view(), name="delete_hourly"),
	url(r'^hourly/add$', ContractHourlyCreate.as_view(), name="add_hourly"),
	url(r'^hourly/(?P<pk>[0-9]+)/edit$', ContractHourlyUpdate.as_view(), name="edit_hourly"),

	# 合同预览相关
	url(r'^preview$', ContractPreviewCodeListView.as_view(), name="list_contractpreviewcode"),
	url(r'^generate$', GeneratePreviewCode.as_view(), name="generate_preview_code"),
	url(r'^preview_pdf$', GeneratePreviewPdf.as_view(), name="pdf"),  # 通过预览码，预览合同条款
	url(r'^download_contract_pdf$', DownloadContractPdf.as_view(), name="download_pdf"),  # 通过预览码，预览合同条款
	url(r'^list$', ContractTypeListView.as_view(), name="list_contract"),
	url(r'^(?P<contract_type>\w+)/download_contract$', DownloadContractView.as_view(), name="download_contract"),
]
