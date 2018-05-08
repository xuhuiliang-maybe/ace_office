# coding=utf-8
import datetime
import json
import os
import random
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views.generic import View

from modules.contract_manage.models import ContractPreviewCode
from modules.share_module.get_path import get_media_sub_path
from modules.share_module.permissionMixin import class_view_decorator


# 生成不同类型合同预览码
@class_view_decorator(login_required)
class GeneratePreviewCode(View):
	def post(self, request, *args, **kwargs):
		result = json.dumps({"code": -1, "msg": u"生成失败"})
		try:
			contract_type = self.request.POST.get("contract_type", "")

			# 生成相应合同预览码
			if contract_type:
				code = contract_type + "".join(map(str, random.sample(range(10), 5)))
				obj = ContractPreviewCode()
				obj.contract_type = contract_type
				obj.code = code
				obj.end_time = timezone.now() + datetime.timedelta(hours=2)
				obj.generate_user = request.user
				obj.save()

				result = json.dumps({"code": 1, "msg": u"预览码 %s" % code})
		except:
			traceback.print_exc()
		finally:
			return HttpResponse(result, content_type="application/json")


# 查看合同-pdf
class GeneratePreviewPdf(View):
	def get(self, request, *args, **kwargs):
		preview_code = request.GET.get("preview_code", "")
		info_template_path = get_media_sub_path("generate_preview")
		file_name = ""

		if preview_code:
			contract_type = preview_code[0]
			contract_obj = ContractPreviewCode.objects.filter(contract_type=contract_type,
									  code=preview_code,
									  end_time__gt=timezone.now())
			if contract_obj.exists():

				if contract_type == "1":
					file_name = "contract-send.pdf"
				if contract_type == "2":
					file_name = "contract-outsourc.pdf"
				if contract_type == "3":
					file_name = "contract-intern.pdf"
				if contract_type == "4":
					file_name = "contract-service.pdf"
				if contract_type == "5":
					file_name = "contract-hourly.pdf"

				contract_obj.update(number=F('number') + 1)

				filepath = os.path.join(info_template_path, file_name)
				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'filename=%s' % file_name
				content = open(filepath, 'rb').read()
				response.write(content)
				return response
		# 没有预览码
		messages.warning(request, u"无效的预览码")
		return TemplateResponse(request, "login.html", {"target": "#forgot-box"})


# 下载合同-pdf
class DownloadContractPdf(View):
	def get(self, request, *args, **kwargs):
		contract_type = request.GET.get("contract_type", "")
		info_template_path = get_media_sub_path("generate_preview")
		file_name = ""

		if contract_type == "1":
			file_name = "labor_contract(paiqian).pdf"
		if contract_type == "2":
			file_name = "contract-outsourc.pdf"
		if contract_type == "3":
			file_name = "contract-intern.pdf"
		if contract_type == "4":
			file_name = "contract-service.pdf"
		if contract_type == "5":
			file_name = "contract-hourly.pdf"

		filepath = os.path.join(info_template_path, file_name)
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=%s' % file_name
		content = open(filepath, 'rb').read()
		response.write(content)
		return response
