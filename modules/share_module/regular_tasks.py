# coding=utf-8
import datetime
import os
import traceback

os.environ['DJANGO_SETTINGS_MODULE'] = 'ace_office.settings'
from config.conf_core import *
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from modules.system.models import SystemConfig, DataBackup
from modules.share_module.get_path import get_media_sub_path
from modules.system.system_backup.backup_add_views import DataBackupCreate

"""
定时任务
Parameters:
    year (int|str) – 4-digit year
    month (int|str) – month (1-12)
    day (int|str) – day of the (1-31)
    week (int|str) – ISO week (1-53)
    day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
    hour (int|str) – hour (0-23)
    minute (int|str) – minute (0-59)
    second (int|str) – second (0-59)
    start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
    end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
    timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
"""


def quote_send_sh_job():
	print 'a simple cron job start at', timezone.now()


def create_backup_job():
	"""定时，备份数据库
	:return:
	"""

	def back_up():
		create_db = DataBackupCreate()
		create_db.backup_db()
		create_db.save_backup_info("system", u"Time Task")

	try:
		scheduled_backup = SystemConfig.get_param('scheduled_backup').get('scheduled_backup', 7) or 7
		createbackupdays = int(scheduled_backup)  # 备份间隔
		last_backup_info = DataBackup.objects.order_by("-id").first()
		if last_backup_info:
			last_backup_time = last_backup_info.starttime
			print (timezone.now() - last_backup_time).days, createbackupdays
			# 当前时间-最后备份时间==备份间隔天数
			if (timezone.now() - last_backup_time).days == createbackupdays and createbackupdays:
				back_up()
		else:
			back_up()
	except:
		traceback.print_exc()


def delete_backup_job():
	"""定时，删除数据库备份
	:return:
	"""
	try:
		scheduled_clean = SystemConfig.get_param('scheduled_clean').get('scheduled_clean', 365) or 365
		delbackupdays = int(scheduled_clean)  # 清备份间隔
		bak_dir = get_media_sub_path("mysql_backup/")  # 备份目录
		del_date = timezone.now() - datetime.timedelta(days=delbackupdays)  # 定时清除备份间隔天之前日期
		del_date_str = del_date.strftime("%Y%m%d%H%M%S")

		if delbackupdays:  # 定时任务不等于默认值0，清备份
			for dirpath, dirnames, filenames in os.walk(bak_dir):
				for one_file in filenames:
					targetFile = os.path.join(dirpath, one_file)
					if os.path.isfile(targetFile) and one_file[0:13] < del_date_str:
						print "delete==", targetFile
						os.remove(targetFile)
	except:
		traceback.print_exc()


from modules.employee_management.employee_info.code.employee_export_views import write_employee_file
from modules.employee_management.employee_info.models import Employee
import time


def export_employee():
	"""定时，导出人员信息
	:return:
	"""
	try:
		file_name = "Employee" + "_" + time.strftime("%Y%m%d%H%M%S") + ".txt"
		tmp_path = get_media_sub_path("export_employee")  # 临时文件夹路径
		filepath = os.path.join(tmp_path, file_name)  # 导出文件路径
		employee_obj_list = Employee.objects.filter(is_temporary=False)
		employee_type = "employee"
		write_employee_file(employee_type, employee_obj_list, filepath)
	except:
		traceback.print_exc()


schedudler = BackgroundScheduler()


def all_tasks():
	try:
		# schedudler.add_job(quote_send_sh_job, 'cron', day_of_week='0-6', hour='0-24', minute='*', second="*/5")
		schedudler.add_job(export_employee, 'cron', day_of_week='0-6', hour='0', minute='0', second="0")
		# schedudler.add_job(delete_backup_job, 'cron', day_of_week='0-6', hour='1', minute='0', second='0')
		# schedudler.add_job(create_backup_job, 'cron', day_of_week='0-6', hour='2', minute='0', second='0')
		try:
			schedudler.start()
		except (KeyboardInterrupt, SystemExit):
			schedudler.shutdown()
	except:
		traceback.print_exc()
