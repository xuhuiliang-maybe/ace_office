# coding=utf-8
import json
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import DeleteView

from config.conf_core import SUPERUSERNAME
from modules.employee_management.employee_info.models import Employee
from modules.share_module.check_decorator import check_principal, check_user_is_songxiaodan
from modules.share_module.permissionMixin import class_view_decorator


# 员工信息-删除
@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.delete_employee', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
@class_view_decorator(check_user_is_songxiaodan)  # 校验是否是songxiaodan
class EmployeeDelete(SuccessMessageMixin, DeleteView):
	model = Employee
	template_name = "base/confirm_delete.html"
	success_message = u"%(name)s 删除创建"

	def get_success_url(self):
		self.url = reverse('employee_info:list', args=("employee",))
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(EmployeeDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context


# 员工信息-批量删除
@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.delete_employee', raise_exception=True))
class EmployeesBatchDelete(SuccessMessageMixin, View):
	def post(self, request, *args, **kwargs):
		try:
			ids = request.POST.get('ids').split(",")
			employee_obj = Employee.objects.filter(is_temporary=False)  # 查询所有正式员工
			if ids[0] == "all":
				if request.user.is_superuser:
					employee_obj.filter(status="1").delete()
					if request.user.username == SUPERUSERNAME:
						employee_obj.all.delete()
					messages.success(self.request, u"成功删除")
					result = {"code": -1, "msg": u"成功删除"}
					return HttpResponse(json.dumps(result), content_type="application/json")
				else:
					emp_obj_list = employee_obj.all()
			else:
				emp_obj_list = employee_obj.filter(id__in=ids)

			for one_obj in emp_obj_list:
				try:
					try:
						project_principal = one_obj.project_name.principal
					except:
						project_principal = None
					if project_principal == request.user or request.user.is_superuser:  # 是项目负责人或超级管理员
						if one_obj.status == "1" or request.user.username == SUPERUSERNAME:  # 员工在职或用户时宋晓丹
							one_obj.delete()
				except:
					traceback.print_exc()

			messages.success(self.request, u"成功删除")
			result = {"code": -1, "msg": u"成功删除"}
		except:
			traceback.print_exc()
			messages.warning(self.request, u"删除操作异常")
			result = {"code": -1, "msg": u"删除异常"}

		return HttpResponse(json.dumps(result), content_type="application/json")


# 临时工-删除
@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.delete_temporary', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class TemporaryDelete(SuccessMessageMixin, DeleteView):
	model = Employee
	template_name = "base/confirm_delete.html"
	success_message = u"%(name)s 删除创建"

	def get_success_url(self):
		self.url = reverse('employee_info:list', args=("temporary",))
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(TemporaryDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context


# 临时工-批量删除
@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.delete_temporary', raise_exception=True))
class TemporaryBatchDelete(SuccessMessageMixin, View):
	def post(self, request, *args, **kwargs):
		try:
			ids = request.POST.get('ids').split(",")
			employee_obj = Employee.objects.filter(is_temporary=True)  # 查询所有临时工
			if ids[0] == "all":
				if request.user.is_superuser:
					employee_obj.all().delete()
					messages.success(self.request, u"成功删除")
					result = {"code": -1, "msg": u"成功删除"}
					return HttpResponse(json.dumps(result), content_type="application/json")
				else:
					emp_obj_list = employee_obj.all()
			else:
				emp_obj_list = employee_obj.filter(id__in=ids)

			for one_obj in emp_obj_list:
				try:
					try:
						project_principal = one_obj.project_name.principal
					except:
						project_principal = None
					if project_principal == request.user or request.user.is_superuser:
						one_obj.delete()
				except:
					traceback.print_exc()

			messages.success(self.request, u"成功删除")
			result = {"code": -1, "msg": u"成功删除"}
		except:
			traceback.print_exc()
			messages.warning(self.request, u"删除操作异常")
			result = {"code": -1, "msg": u"删除异常"}

		return HttpResponse(json.dumps(result), content_type="application/json")
