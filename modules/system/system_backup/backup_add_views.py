# coding=utf-8
import json
import time
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
@class_view_decorator(permission_required('databackup.add_databackup', raise_exception=True))
class DataBackupCreate(View):
	def post(self, request, *args, **kwargs):
		try:
			self.backup_db()

			# 指令执行成功
			if self.bak_result == 0:
				user_name = request.user.username
				user_first_name = request.user.first_name
				self.save_backup_info(user_name, user_first_name)
				result = json.dumps({"code": 1, "msg": u"备份成功"})
			else:
				result = json.dumps({"code": -1, "msg": str(self.bak_result) + u" 备份失败!"})

			return HttpResponse(result, content_type="application/json")
		except:
			traceback.print_exc()

	def backup_db(self):
		try:
			# 备份目录，不存在就创建
			bak_dir = get_media_sub_path("mysql_backup/")
			if not os.path.exists(bak_dir):
				os.makedirs(bak_dir)

			# 备份路径+备份文件名
			self.bak_db_name = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + ".sql"
			bak_dir_db_name = os.path.join(bak_dir, self.bak_db_name)

			# 执行备份
			self.bak_start_time = timezone.now()
			bak_shell = "mysqldump --add-drop-table -h" + DB_HOST + " -u" + DB_USERNAME + " -p" + DB_PASSWORD + " " + DB_NAME + " > " + bak_dir_db_name
			self.bak_result = os.system(bak_shell)
			self.bak_end_time = timezone.now()
			print "back shell==" + bak_shell
			print "os.system result==", self.bak_result
		except:
			traceback.print_exc()

	def save_backup_info(self, user_name, user_first_name):
		try:

			add_bak_param = {
				"databasetype": DB_ENGINE,
				"backupdatabase": self.bak_db_name,
				"starttime": self.bak_start_time,
				"endtime": self.bak_end_time,
				"status": "1",
				"operator": user_first_name,
			}
			DataBackup(**add_bak_param).save()
		except:
			traceback.print_exc()
