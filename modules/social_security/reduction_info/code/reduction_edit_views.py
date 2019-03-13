# coding=utf-8
import json
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import UpdateView

from modules.organizational_structure.departments.models import Department
from modules.share_module.check_decorator import check_principal
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from modules.social_security.check_info_expire import check_expire
from modules.social_security.reduction_info.models import Reduction


@class_view_decorator(login_required)
@class_view_decorator(permission_required('reduction_info.change_reduction', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
@class_view_decorator(check_expire)  # 校验是否到期
class ReductionUpdate(SuccessMessageMixin, UpdateView):
	"""编辑减员信息
	"""
	model = Reduction
	template_name = "base/document_edit.html"
	success_message = u"%(emplyid)s 成功修改"
	fields = ["emplyid", "dept_verify", "complete_verify", "remark", "remark1", "remark2"]

	def get_success_url(self):
		self.url = reverse('reduction_info:reduction_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('reduction_info:reduction_add')
		return self.url

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(ReductionUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改减员信息"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context


@class_view_decorator(login_required)
@class_view_decorator(permission_required('reduction_info.change_reduction', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class ReductionUpdateRemark(SuccessMessageMixin, UpdateView):
	"""编辑减员信息备注信息
	"""
	template_name = "base/document_edit.html"
	model = Reduction
	success_message = u"%(emplyid)s 成功修改"
	fields = ["remark", "remark1", "remark2"]

	def get_success_url(self):
		self.url = reverse('reduction_info:reduction_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(ReductionUpdateRemark, self).get_context_data(**kwargs)
		context["form_content"] = u"减员信息到期，只提供添加备注"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context


@class_view_decorator(login_required)
@class_view_decorator(permission_required('reduction_info.change_increase', raise_exception=True))
class ReductionCustomUpdate(View):
	"""编辑减员信息，针对：部门确认，最终确认
	"""

	def post(self, request, *args, **kwargs):
		result = dict()
		try:
			oper_type = request.POST.get("oper_type", "")  # 操作类型，batch_oper：批处理
			pk_str = request.POST.get("pk", "")  # 以逗号分割，兼容批量确认
			pk_list = pk_str.split(",")
			filed = request.POST.get("filed", "")
			verify_value = request.POST.get("verify_value", "")
			login_user = request.user

			if oper_type == "batch_oper":
				for one_pk in pk_list:
					# 判断权限
					# 部门确认：只能由员工部门经理来操作，dept_verify
					if filed == "dept_verify":
						if one_pk:
							reduction_obj = Reduction.objects.filter(id=one_pk)
						try:
							if reduction_obj.exists():
								check_pass = 0
								# 非客服部的项目，由人事部负责人做部门确认
								customer_service_dept = Department.objects.filter(name=u"客服部")
								all_customer_service_dept = list()
								if customer_service_dept.exists():
									all_customer_service_dept = customer_service_dept[0].all_children()
								if reduction_obj[0].emplyid.project_name.department not in all_customer_service_dept:
									#  当前信息部门，不属于客服部
									personnel_dept_principal = User.objects.filter(attribution_dept=u"人事部", dept_head=True)  # 人事部负责人
									if login_user not in personnel_dept_principal:
										result["msg"] = u"部分非客服部项目，只能由人事部负责人做确认，权限不足"
										result["code"] = 0
										continue
										# return HttpResponse(json.dumps(result), content_type="application/json")
									else:
										check_pass = 1

								# 客服经理
								if not check_pass:
									customer_service_director = reduction_obj[0].emplyid.project_name.customer_service_director
									if login_user != customer_service_director:
										result["msg"] = u"部分非项目客服经理，权限不足"
										result["code"] = 0
										continue
										# return HttpResponse(json.dumps(result), content_type="application/json")

						except:
							traceback.print_exc()
							continue
							# result["msg"] = u"权限不足"
							# result["code"] = 0
							# return HttpResponse(json.dumps(result), content_type="application/json")

					# 最终确认：只能由社保专员操作，complete_verify
					if filed == "complete_verify":
						try:
							if login_user.position.name != u"社保专员":
								result["msg"] = u"只能由社保专员操作，权限不足"
								result["code"] = 0
								return HttpResponse(json.dumps(result), content_type="application/json")
						except:
							traceback.print_exc()
							result["msg"] = u"权限不足"
							result["code"] = 0
							return HttpResponse(json.dumps(result), content_type="application/json")

					search_condition = {filed: verify_value}
					kwargs = get_kwargs(search_condition)
					Reduction.objects.filter(id=one_pk).update(**kwargs)

					result["msg"] = u"成功设置"
					result["code"] = 1

			if not oper_type:
				# 判断权限
				# 部门确认：只能由员工部门经理来操作，dept_verify
				if filed == "dept_verify":
					reduction_obj = Reduction.objects.filter(id=pk_list[0])
					try:
						if reduction_obj.exists():
							check_pass = 0
							# 非客服部的项目，由人事部负责人做部门确认
							customer_service_dept = Department.objects.filter(name=u"客服部")
							all_customer_service_dept = list()
							if customer_service_dept.exists():
								all_customer_service_dept = customer_service_dept[
									0].all_children()
							if reduction_obj[
								0].emplyid.project_name.department not in all_customer_service_dept:
								#  当前信息部门，不属于客服部
								personnel_dept_principal = User.objects.filter(
									attribution_dept=u"人事部", dept_head=True)  # 人事部负责人
								if login_user not in personnel_dept_principal:
									result["msg"] = u"非客服部项目，只能由人事部负责人做确认，权限不足"
									result["code"] = 0
									return HttpResponse(json.dumps(result),
											    content_type="application/json")
								else:
									check_pass = 1

							# 客服经理
							if not check_pass:
								customer_service_director = reduction_obj[
									0].emplyid.project_name.customer_service_director
								if login_user != customer_service_director:
									result["msg"] = u"非项目客服经理，权限不足"
									result["code"] = 0
									return HttpResponse(json.dumps(result),
											    content_type="application/json")

					except:
						traceback.print_exc()
						result["msg"] = u"权限不足"
						result["code"] = 0
						return HttpResponse(json.dumps(result), content_type="application/json")

				# 最终确认：只能由社保专员操作，complete_verify
				if filed == "complete_verify":
					try:
						if login_user.position.name != u"社保专员":
							result["msg"] = u"只能由社保专员操作，权限不足"
							result["code"] = 0
							return HttpResponse(json.dumps(result), content_type="application/json")
					except:
						traceback.print_exc()
						result["msg"] = u"权限不足"
						result["code"] = 0
						return HttpResponse(json.dumps(result), content_type="application/json")

				search_condition = {filed: verify_value}
				kwargs = get_kwargs(search_condition)
				Reduction.objects.filter(id=pk_list[0]).update(**kwargs)
				result["msg"] = u"成功设置"
				result["code"] = 1
		except:
			traceback.print_exc()
			result["msg"] = u"保存失败!"
			result["code"] = 0

		return HttpResponse(json.dumps(result), content_type="application/json")
