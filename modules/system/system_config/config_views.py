# coding=utf-8
import json
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View

from modules.share_module.permissionMixin import class_view_decorator
from modules.system.models import SystemConfig


@class_view_decorator(login_required)
@class_view_decorator(permission_required('system.browse_systemconfig', raise_exception=True))
class SystemConfigListView(View):
	def get(self, request, *args, **kwargs):
		try:
			param_list = SystemConfig.objects.all()
			template_name = "system_config.html"
			return render_to_response(template_name,
						  {"param_list": param_list},
						  context_instance=RequestContext(request))
		except:
			traceback.print_exc()


@class_view_decorator(login_required)
@class_view_decorator(permission_required('system.change_systemconfig', raise_exception=True))
class SystemConfigUpdateView(View):
	def post(self, request, *args, **kwargs):
		result = dict()
		try:
			param_name = request.POST.get("name", "")
			param_value = request.POST.get("newvalue", "")
			SystemConfig.objects.filter(param_name=param_name).update(param_value=param_value)
			result["msg"] = "成功设置"
		except:
			traceback.print_exc()
			result["msg"] = "保存失败!"

		return HttpResponse(json.dumps(result), content_type="application/json")
