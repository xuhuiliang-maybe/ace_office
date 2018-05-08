# coding=utf-8
from django.conf.urls import url

from modules.social_security.reduction_info.code import reduction_views, reduction_add_views, reduction_edit_views, \
	reduction_delete

# 减员信息
urlpatterns = [
	url(r'^list$', reduction_views.ReductionListView.as_view(), name="reduction_list"),
	url(r'^reduction_add$', reduction_add_views.ReductionCreate.as_view(), name="reduction_add"),
	url(r'^reduction_(?P<pk>[0-9]+)/edit$', reduction_edit_views.ReductionUpdate.as_view(), name="reduction_edit"),
	url(r'^reduction_(?P<pk>[0-9]+)/edit_remark$', reduction_edit_views.ReductionUpdateRemark.as_view(),
	    name="reduction_edit_remark"),
	url(r'^reduction_(?P<pk>[0-9]+)/delete$', reduction_delete.ReductionDelete.as_view(), name="reduction_delete"),
	url(r'^reduction/batchdelete$', reduction_delete.ReductionBatchDelete.as_view(), name="reduction_batch_delete"),
	# 批量删除
	url(r'^update$', reduction_edit_views.ReductionCustomUpdate.as_view(), name='reduction_update'),

]
