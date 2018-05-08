# coding=utf-8
import json
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import View

from config.conf_core import *
from modules.share_module.get_path import get_media_sub_path
from modules.share_module.permissionMixin import class_view_decorator
from modules.system.models import DataBackup


@class_view_decorator(login_required)
@class_view_decorator(permission_required('databackup.reduct_databackup', raise_exception=True))
class DataBackupReduction(View):
	def post(self, request, *args, **kwargs):
		try:
			# 备份目录，不存在就创建
			bak_dir = get_media_sub_path("mysql_backup/")
			if not os.path.exists(bak_dir):
				os.makedirs(bak_dir)

			backup_objs = DataBackup.objects.filter(**kwargs)
			if backup_objs.exists():
				backup_obj = backup_objs[0]
				back_file_name = backup_obj.backupdatabase
				bak_dir_db_name = os.path.join(bak_dir, back_file_name)

				if not os.path.exists(bak_dir_db_name):
					result = {"code": -1, "msg": u"备份信息不存在"}
					return HttpResponse(json.dumps(result), content_type="application/json")

				reduct_shell = "mysql -h" + DB_HOST + " -u" + DB_USERNAME + " -p" + DB_PASSWORD + " " + DB_NAME + " < " + bak_dir_db_name
				reduct_result = os.system(reduct_shell)
				print "back shell==" + reduct_shell
				print "os.system result==", reduct_result

				# 指令执行成功
				if reduct_result == 0:
					update_param = {
						"databasetype": backup_obj.databasetype,
						"backupdatabase": backup_obj.backupdatabase,
						"starttime": backup_obj.starttime,
						"endtime": backup_obj.endtime,
						"reduct_time": timezone.now(),
						"status": "2",
						"operator": request.user.first_name,
					}
					DataBackup.objects.create(**update_param)
					result = {"code": 1, "msg": u"还原成功"}
				else:
					result = {"code": -1, "msg": str(reduct_result) + u" 还原失败!"}
			else:
				result = {"code": -1, "msg": u"备份信息不存在"}

			return HttpResponse(json.dumps(result), content_type="application/json")
		except:
			traceback.print_exc()
