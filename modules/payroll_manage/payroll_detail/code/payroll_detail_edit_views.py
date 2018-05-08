# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.payroll_manage.payroll_detail.models import PayrollDetail
from modules.share_module.check_decorator import check_principal
from modules.share_module.permissionMixin import class_view_decorator

"""
薪资明细，编辑
"""


@class_view_decorator(login_required)
@class_view_decorator(permission_required('payroll_detail.change_payrolldetail', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class PayrollDetailUpdate(SuccessMessageMixin, UpdateView):
	model = PayrollDetail
	template_name = "payroll_edit.html"
	success_message = u"%(name)s 成功修改"
	fields = "__all__"

	def get_success_url(self):
		self.url = reverse('payroll_manage:payroll_detail:payroll_detail_list', args=())

		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('payroll_manage:payroll_detail:payroll_detail_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(PayrollDetailUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改薪资明细"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
