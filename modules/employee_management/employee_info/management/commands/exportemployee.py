# coding=utf-8
from django.core.management.base import BaseCommand, CommandError

from modules.employee_management.employee_info.code.employee_export_views import *
from modules.share_module.export import *
from modules.share_module.formater import *
import datetime


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
			kwargs = dict()
			if employee_type == "employee":  # 查看员工信息
				kwargs.update({"is_temporary": False})
			elif employee_type == "temporary":  # 查看临时工信息
				kwargs.update({"is_temporary": True})
			employee_obj_list = Employee.objects.filter(**kwargs)
			total = employee_obj_list.count()
			file_path, file_name = write_excel(employee_type, employee_obj_list)

			# 上传百度云
			# 判断文件是否存在
			if os.path.exists(file_path):
				# os.system("bypy mkdir ExportEmployee")
				os.system("bypy upload %s ExportEmployee -v" % file_path)

			print 'Export full employee information to %s；Total %s；%s \n' % (
				file_name, str(total), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

		except:
			traceback.print_exc()
			raise CommandError(traceback.format_exc())
