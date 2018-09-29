# coding=utf-8
import gc
import subprocess

from django.core.management.base import BaseCommand, CommandError

from modules.employee_management.employee_info.code.employee_export_views import *
from modules.share_module.export import *
from modules.share_module.formater import *


class Command(BaseCommand):
	help = "Export full employee information to Excel"

	def handle(self, *args, **options):
		"""定时导出所有员工信息
		:return:
		"""
		try:
			print "\n"
			print "Start %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			employee_type = "employee"
			kwargs = {"is_temporary": False}
			# if employee_type == "employee":  # 查看员工信息
			# 	kwargs.update({"is_temporary": False})
			# elif employee_type == "temporary":  # 查看临时工信息
			# 	kwargs.update({"is_temporary": True})
			employee_obj_list = Employee.objects.filter(**kwargs)
			total = employee_obj_list.count()
			file_path, file_name = write_excel(employee_type, employee_obj_list)

			# 上传百度云
			# 判断文件是否存在
			print file_path, os.path.exists(file_path)

			gc.collect()
			if os.path.exists(file_path):
				# os.system("bypy mkdir ExportEmployee")
				# os.system("/usr/local/bin/bypy upload %s ExportEmployee -v" % file_path)
				command_str = "/var/www/html/bpcs_uploader/bpcs_uploader.php upload %s ExportEmployee/%s" % (
					file_path, file_name)
				os.system(command_str)
			print "Total %s" % str(total)
			print "End %s \n" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		except:
			traceback.print_exc()
			raise CommandError(traceback.format_exc())

"""
链接: https://pan.baidu.com/s/1pKfFJvLuwGxcfTGF0LvjNQ 提取码: iysd
"""
