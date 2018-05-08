# coding=utf-8
from django.conf.urls import url

from modules.system.system_backup import backup_add_views
from modules.system.system_backup import backup_reduction_views
from modules.system.system_backup import backup_views
from modules.system.system_backup import delete_backup_views
from modules.system.system_backup import download_backup_views
from modules.system.system_config import config_views

# 系统相关
urlpatterns = [
	url(r'^config$', config_views.SystemConfigListView.as_view(), name='config-list'),  # 系统配置
	url(r'^config/update$', config_views.SystemConfigUpdateView.as_view(), name='config-update'),  # 系统配置

	url(r'^data_backup$', backup_views.BackupListView.as_view(), name='data_backup'),  # 备份列表
	url(r'^data_backup_add$', backup_add_views.DataBackupCreate.as_view(), name='data_backup_add'),  # 新增备份

	url(r'^data_backup/(?P<pk>[0-9]+)/delete$', delete_backup_views.DataBackupDelete.as_view(),
	    name='data_backup_delete'),  # 删除备份

	url(r'^data_backup/(?P<pk>[0-9]+)/download$', download_backup_views.DataBackupDownload.as_view(),
	    name='data_backup_download'),  # 下载备份

	url(r'^data_backup/(?P<pk>[0-9]+)/reduction$', backup_reduction_views.DataBackupReduction.as_view(),
	    name='data_backup_reduction'),  # 还原备份

]
