# coding=utf-8
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView

from ace_office import settings
from modules.home_page.code import homepage_views
from modules.share_module.download import DownloadInfoTemplateView
from modules.sidebar_menu.code.menus_list_views import SidebarMenusList

handler500 = "ace_office.views.redirect_500_error"
handler404 = "ace_office.views.redirect_404_error"
handler403 = "ace_office.views.redirect_403_error"
handler400 = "ace_office.views.redirect_400_error"

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	# url(r'^messages/', include('monitio.urls', namespace="monitio")),  # 实时消息
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_PATH}),  # 静态文件
	url(r'^getmenubyuser/$', SidebarMenusList.as_view(), name='getmenubyuser'),  # 获取用户菜单栏
	url(r'^maintenance$', TemplateView.as_view(template_name="system_maintenance.html")),  # 维护状态
	url(r'^prompt$', TemplateView.as_view(template_name="prompt.html"), name="prompt"),  # 提示

	# 下载信息模板excel
	url(r'^download/(?P<template_name>\w+)$', DownloadInfoTemplateView.as_view(), name="download"),

	# 登录权限
	url(r'^accounts/', include('modules.admin_account.urls', namespace='admin_account')),

	# 我的主页-统计图表
	url(r'^$', homepage_views.IndexView.as_view(), name="home_page"),
	url(r'^homepage/', include('modules.home_page.urls', namespace='home_page')),

	# 我的地盘
	url(r'^mysite/', include('modules.mysite.urls', namespace='mysite')),

	# 组织架构
	url(r'^organizational/', include('modules.organizational_structure.urls', namespace='organizational_structure')),

	# 项目管理
	url(r'^projectmanage/', include('modules.project_manage.urls', namespace='project_manage')),

	# 员工管理
	url(r'^employeemanage/', include('modules.employee_management.employee_info.urls', namespace='employee_info')),

	# 档案信息
	url(r'^archive/', include('modules.employee_management.archives_info.urls', namespace='archive_info')),

	# 社保福利增员
	url(r'^increase/', include('modules.social_security.increase_info.urls', namespace='increase_info')),
	# 社保福利减员
	url(r'^reduction/', include('modules.social_security.reduction_info.urls', namespace='reduction_info')),
	# 社保明细
	url(r'^social_security_detail/',
	    include('modules.social_security.social_security_detail.urls', namespace='social_security_detail')),

	# 结算发薪
	url(r'^payroll/', include('modules.settlement_pay.urls', namespace='settlement_pay')),

	# 招聘管理
	url(r'^recruitment/', include('modules.recruitment_manage.urls', namespace='recruitment')),

	# 审批流程
	url(r'^approval/', include('modules.approval_process.urls', namespace='approval')),

	# 费用管理
	url(r'^expense/', include('modules.expense_manage.urls', namespace='expense_manage')),

	# 人事操作质量
	url(r'^personnel/', include('modules.personnel_operation.urls', namespace='personnel_info')),

	# 薪资管理
	url(r'^payroll_manage/', include('modules.payroll_manage.urls', namespace='payroll_manage')),

	# 财务
	url(r'^finance/', include('modules.finance.urls', namespace='finance')),

	# 合同管理
	url(r'^contract/', include('modules.contract_manage.urls', namespace='contract')),

	# 考勤
	# url(r'^attendance/', include('modules.attendance.urls', namespace='attendance')),

	# 系统相关
	url(r'^system/', include('modules.system.urls', namespace='system')),

	# 字典表相关
	url(r'^dicttable/', include('modules.dict_table.urls', namespace='dicttable')),

	# 二维码
	url(r'^qrcode/(.+)$', 'modules.mysite.views.generate_qrcode', name='qrcode'),
]

# 照片相关
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
