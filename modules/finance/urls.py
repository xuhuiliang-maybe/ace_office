# coding=utf-8
from django.conf.urls import include, url

# 财务
urlpatterns = [
	# 社保审批
	url(r'^social_security_audit/',
	    include('modules.finance.social_security_audit.urls', namespace='social_security_audit')),

	# 到账与开票
	url(r'^arrival_and_billing/',
	    include('modules.finance.arrival_and_billing.urls', namespace="arrival_and_billing")),

	# 借款与销账
	url(r'^loans_and_write_offs/',
	    include('modules.finance.loans_and_write_offs.urls', namespace='loans_and_write_offs')),
]
