# coding=utf-8
from django.conf.urls import url

from modules.finance.loans_and_write_offs.code.del_loans_and_write_offs import *
from modules.finance.loans_and_write_offs.code.edit_loans_and_write_offs import *
from modules.finance.loans_and_write_offs.code.export_loans_and_write_offs import *
from modules.finance.loans_and_write_offs.code.list_loans_and_write_offs import *

# 财务-借款与销账
urlpatterns = [
	# url(r'^add$', LoansAndWriteOffsCreate.as_view(), name="add_loansandwriteoffs"),  # 增
	url(r'^(?P<pk>[0-9]+)/delete$', LoansAndWriteOffsDelete.as_view(), name="del_loansandwriteoffs"),  # 删
	url(r'^list$', LoansAndWriteOffsListView.as_view(), name="list_loansandwriteoffs"),  # 查
	url(r'^(?P<pk>[0-9]+)/edit$', LoansAndWriteOffsUpdate.as_view(), name="edit_loansandwriteoffs"),  # 改
	url(r'^export$', LoansAndWriteOffsExportView.as_view(), name="export_loansandwriteoffs"),  # 导出
]
