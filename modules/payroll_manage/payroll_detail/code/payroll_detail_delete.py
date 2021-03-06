# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import DeleteView

from modules.payroll_manage.payroll_detail.models import PayrollDetail
from modules.share_module.check_decorator import check_principal
from modules.share_module.permissionMixin import class_view_decorator


# 删除薪资明细
@class_view_decorator(login_required)
@class_view_decorator(permission_required('payroll_detail.delete_payrolldetail', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class PayrollDetailDelete(SuccessMessageMixin, DeleteView):
	model = PayrollDetail
	template_name = "base/confirm_delete.html"
	success_message = u"%(name)s 删除创建"

	def get_success_url(self):
		self.url = reverse('payroll_manage:payroll_detail:payroll_detail_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(PayrollDetailDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
