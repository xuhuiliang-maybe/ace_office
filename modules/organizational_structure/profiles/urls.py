# coding=utf-8
from django.conf.urls import url

from modules.organizational_structure.profiles.code import (
	profile_views,
	profile_delete,
	profile_add_views,
	profile_edit_views,
	profile_upload_photo_views,
	profile_export_views,
	profile_load_views,
)

# 用户信息
urlpatterns = [
	url(r'^upload$', profile_upload_photo_views.ProfileUploadPhotoView.as_view(), name="profile_upload"),
	# 上传管理员照片, 待完善
	url(r'^export$', profile_export_views.ProfileExportView.as_view(), name="profile_export"),  # 导出
	url(r'^load$', profile_load_views.ProfileLoadView.as_view(), name="profile_load"),  # 导入


	url(r'^list$', profile_views.ProfileList.as_view(), name="profile_list"),  # 列表
	url(r'^add$', profile_add_views.ProfileCreate.as_view(), name="profile_add"),  # 新增
	url(r'^(?P<pk>[0-9]+)/edit$', profile_edit_views.ProfileUpdate.as_view(), name="profile_edit"),  # 编辑
	url(r'^(?P<pk>[0-9]+)/delete$', profile_delete.ProfileDelete.as_view(), name="profile_delete"),  # 删除
]
