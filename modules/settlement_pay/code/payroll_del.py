# coding=utf-8
import json
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import DeleteView
from django.views.generic import View

from modules.settlement_pay.models import Payroll
from modules.share_module.check_decorator import check_principal
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('settlement_pay.delete_payroll', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class PayrollDelete(SuccessMessageMixin, DeleteView):
	model = Payroll
	template_name = "base/confirm_delete.html"
	success_message = u"%(employee)s 删除创建"

	def get_success_url(self):
		self.url = reverse('settlement_pay:payroll_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(PayrollDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context


@class_view_decorator(login_required)
@class_view_decorator(permission_required('settlement_pay.delete_payroll', raise_exception=True))
class PayrollBatchDelete(SuccessMessageMixin, View):
	def post(self, request, *args, **kwargs):
		try:
			ids = request.POST.get('ids').split(",")
			payroll_obj_list = Payroll.objects.filter(id__in=ids)
			for one_obj in payroll_obj_list:
				try:
					if one_obj.employee.project_name.principal == request.user:
						one_obj.delete()
				except:
					traceback.print_exc()
			messages.success(self.request, u"成功删除")
			result = {"code": 1, "msg": "成功删除"}
		except:
			traceback.print_exc()
			messages.warning(self.request, u"删除操作异常")
			result = {"code": -1, "msg": "删除异常"}

		return HttpResponse(json.dumps(result), content_type="application/json")
