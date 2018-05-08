# coding=utf-8
import os
import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import View

from modules.share_module.get_path import *
from modules.share_module.permissionMixin import class_view_decorator


# 参考并修改
def download_file(filepath, filename, remove=False, content_type="application/ms-excel"):
	"""
	:param filepath:文件全路径，带文件名
	:param filename: 文件名
	:param remove: 是否删除源文件
	:return:
	"""
	try:
		# 设置response
		response = HttpResponse(content_type=content_type)
		response['Content-Disposition'] = 'attachment; filename=' + filename
		# 读取文件
		with open(filepath, "rb") as open_file:
			read_file = open_file.read()
		response.write(read_file)

		# 是否从服务器删除文件
		if remove:
			os.remove(filepath)
		return response
	except:
		traceback.print_exc()


@class_view_decorator(login_required)
class DownloadInfoTemplateView(View):
	"""下载导入模板公用视图 """

	def get(self, request, *args, **kwargs):
		try:
			template_name = kwargs.get('template_name', "")  # 模板名字

			# 下载文件名，路径
			filename = "".join([template_name, ".xlsx"])
			info_template_path = get_media_sub_path("info_template")
			filepath = os.path.join(info_template_path, filename)

			# 页面下载导出文件
			response = download_file(filepath, filename, remove=False)
			return response
		except:
			traceback.print_exc()
