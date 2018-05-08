# coding=utf-8
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View

from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('admin_account.browse_personal', raise_exception=True))
class PersonalListView(View):
	def get(self, request, *args, **kwargs):
		try:
			template_name = "personal_info.html"
			return render_to_response(template_name, {}, context_instance=RequestContext(request))
		except:
			traceback.print_exc()

	def post(self, request, *args, **kwargs):
		try:
			pass
		except:
			traceback.print_exc()

	def update_result_list(self, result_list, one_dept_dict):
		try:
			pass
		except:
			traceback.print_exc()


@class_view_decorator(login_required)
# @class_view_decorator(permission_required('approval_process.change_pendingapproval', raise_exception=True))
class PersonalUpdateView(View):
	""" 编辑登陆用户个人信息 """

	def post(self, request, *args, **kwargs):
		try:
			name = self.request.POST.get("name", "")  # 编辑字段名
			pk = int(self.request.POST.get("pk", 0))  # 编辑用户id，当前登录用户id
			value = self.request.POST.get("value", "")  # 参数值

			login_user = self.request.user
			login_user_id = login_user.id
			if login_user_id == pk:  # 编辑的是同一个人
				kwargs = {name: value}
				User.objects.update(**kwargs)
				return HttpResponse(u"操作成功！")

			return HttpResponse(u"操作失败！")
		except:
			traceback.print_exc()
			return HttpResponse(u"操作异常！")
