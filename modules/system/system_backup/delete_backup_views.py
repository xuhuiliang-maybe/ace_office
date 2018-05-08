# coding=utf-8
import json
import os
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.views.generic import View

from modules.share_module.get_path import get_media_sub_path
from modules.share_module.permissionMixin import class_view_decorator
from modules.system.models import DataBackup


@class_view_decorator(login_required)
@class_view_decorator(permission_required('databackup.delete_databackup', raise_exception=True))
class DataBackupDelete(View):
	def post(self, request, *args, **kwargs):
		try:
			backup_obj = DataBackup.objects.filter(**kwargs)

			bak_dir = get_media_sub_path("mysql_backup/")
			if backup_obj.exists():
				backup_file_name = backup_obj[0].backupdatabase
				bak_dir_db_name = os.path.join(bak_dir, backup_file_name)
				if os.path.isfile(bak_dir_db_name):
					os.remove(bak_dir_db_name)

				backup_obj.delete()
				result = json.dumps({"code": 1, "msg": u"成功删除 "})
			else:
				result = json.dumps({"code": 1, "msg": u"删除失败，备份信息不存在！"})

			return HttpResponse(result, content_type="application/json")
		except:
			traceback.print_exc()
