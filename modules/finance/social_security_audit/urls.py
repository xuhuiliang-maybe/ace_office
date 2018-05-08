# coding=utf-8
from django.conf.urls import url

from modules.finance.social_security_audit.code.add_social_security_audit import *
from modules.finance.social_security_audit.code.del_social_security_audit import *
from modules.finance.social_security_audit.code.edit_social_security_audit import *
from modules.finance.social_security_audit.code.export_social_security_audit import *
from modules.finance.social_security_audit.code.list_social_security_audit import *

# 财务-社保审核
urlpatterns = [
	url(r'^add$', SocialSecurityAuditCreate.as_view(), name="add_socialsecurityaudit"),  # 增
	url(r'^(?P<pk>[0-9]+)/delete$', SocialSecurityAuditDelete.as_view(), name="del_socialsecurityaudit"),  # 删
	url(r'^list$', SocialSecurityAuditListView.as_view(), name="list_socialsecurityaudit"),  # 查
	url(r'^(?P<pk>[0-9]+)/edit$', SocialSecurityAuditUpdate.as_view(), name="edit_socialsecurityaudit"),  # 改
	url(r'^export$', SocialSecurityAuditExportView.as_view(), name="export_socialsecurityaudit"),  # 导出
]
