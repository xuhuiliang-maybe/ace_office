# coding=utf-8
from django.conf.urls import url

from modules.social_security.social_security_detail.code import (
	social_security_detail_add_views,
	social_security_detail_delete_views,
	social_security_detail_list_views,
	social_security_detail_edit_views,
	export_social_security_detail,
	load_social_security_detail
)
from modules.social_security.social_security_detail.models import SocialSecurityDetail

# 社保明细
urlpatterns = [
	# 增
	url(r'^social_security_detail_add$', social_security_detail_add_views.SocialSecurityDetailCreate.as_view(),
	    name="social_security_detail_add"),

	# 删
	url(r'^social_security_detail_(?P<pk>[0-9]+)/delete$',
	    social_security_detail_delete_views.SocialSecurityDetailDelete.as_view(),
	    {"model_name": SocialSecurityDetail}, name="social_security_detail_delete"),
	# 批量
	url(r'^social_security_detail/batchdelete$',
	    social_security_detail_delete_views.SocialSecurityDetailBatchDelete.as_view(),
	    name="social_security_detail_batch_delete"),

	# 查
	url(r'^list$', social_security_detail_list_views.SocialSecurityDetailListView.as_view(), name="reduction_list"),

	# 改
	url(r'^social_security_detail_(?P<pk>[0-9]+)/edit$', social_security_detail_edit_views.IncreaseUpdate.as_view(),
	    {"model_name": SocialSecurityDetail}, name="social_security_detail_edit"),

	# 导出招聘统计
	url(r'^social_security_detail/export$', export_social_security_detail.SocialSecurityDetailExportView.as_view(),
	    name="social_security_detail_export"),

	# 导入招聘统计
	url(r'^social_security_detail/load$', load_social_security_detail.SocialSecurityDetailLoadView.as_view(),
	    name="social_security_detail_load"),

]
