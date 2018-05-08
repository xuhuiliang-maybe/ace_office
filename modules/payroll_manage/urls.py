# coding=utf-8
from django.conf.urls import url, include

# 费用管理相关
urlpatterns = [
	url(r'^detail/', include('modules.payroll_manage.payroll_detail.urls', namespace='payroll_detail')),  # 薪资明细
	url(r'^gather/', include('modules.payroll_manage.payroll_gather.urls', namespace='payroll_gather')),  # 薪资汇总

]
