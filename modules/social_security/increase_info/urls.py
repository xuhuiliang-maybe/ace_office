# coding=utf-8
from django.conf.urls import url

from modules.social_security.increase_info.code import increase_views, increase_add_views, increase_edit_views, \
	increase_delete

# 增员信息
urlpatterns = [
	url(r'^list$', increase_views.IncreaseListView.as_view(), name="increase_list"),
	url(r'^increase_add$', increase_add_views.IncreaseCreate.as_view(), name="increase_add"),
	url(r'^increase_(?P<pk>[0-9]+)/edit$', increase_edit_views.IncreaseUpdate.as_view(), name="increase_edit"),  # 编辑
	url(r'^increase_(?P<pk>[0-9]+)/edit_remark$', increase_edit_views.IncreaseUpdateRemark.as_view(),  # 编辑备注信息
	    name="increase_edit_remark"),
	url(r'^increase_(?P<pk>[0-9]+)/delete$', increase_delete.IncreaseDelete.as_view(), name="increase_delete"),
	url(r'^increase/batchdelete$', increase_delete.IncreaseBatchDelete.as_view(), name="increase_batch_delete"),
	# 批量删除
	url(r'^update$', increase_edit_views.IncreaseCustomUpdate.as_view(), name='increase_update'),

]
