# coding=utf-8
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import View

from modules.share_module.download import download_file
from modules.share_module.get_path import get_media_sub_path
from modules.share_module.permissionMixin import class_view_decorator
from modules.system.models import DataBackup


@class_view_decorator(login_required)
@class_view_decorator(permission_required('databackup.download_databackup', raise_exception=True))
class DataBackupDownload(View):
	def get(self, request, *args, **kwargs):
		try:
			backup_obj = DataBackup.objects.filter(**kwargs)
			filepath = get_media_sub_path("mysql_backup/")
			filename = ""
			if backup_obj.exists():
				filename = backup_obj[0].backupdatabase
				filepath += filename

			# 页面下载导出文件
			response = download_file(filepath, filename, False)
			return response
		except:
			traceback.print_exc()
