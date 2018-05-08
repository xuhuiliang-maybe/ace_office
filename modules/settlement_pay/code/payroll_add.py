# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.settlement_pay.models import Payroll
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('settlement_pay.add_payroll', raise_exception=True))
class PayrollCreate(SuccessMessageMixin, CreateView):
	model = Payroll
	template_name = "payroll_edit.html"
	success_message = u"%(employee)s 成功创建"
	fields = "__all__"

	def get_success_url(self):
		self.url = reverse('settlement_pay:payroll_list', args=())
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('settlement_pay:payroll_add')
		return self.url

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(PayrollCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"新增结算发薪"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
