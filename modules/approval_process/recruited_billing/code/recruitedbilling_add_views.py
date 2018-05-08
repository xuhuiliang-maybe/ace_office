# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.approval_process.recruited_billing.models import *
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('recruited_billing.add_recruitedbilling', raise_exception=True))
class RecruitedBillingCreate(SuccessMessageMixin, CreateView):
	template_name = "recruited_billing_edit.html"
	model = RecruitedBilling
	success_message = u"%(title)s 成功申请"
	fields = ["title", "note", "project_name", "billing_month", "settlement_amount", "is_billing", "content"]

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(RecruitedBillingCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"待招结算与开票申请"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	# 将登陆用户作为申请人
	def form_valid(self, form):
		form.instance.apply_user = self.request.user
		form.instance.apply_types = "9"  # 申请类型，参考模型
		return super(RecruitedBillingCreate, self).form_valid(form)

	def get_success_url(self):
		self.url = reverse('approval:recruitedbilling_list')
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:recruitedbilling_add')
		return self.url


@class_view_decorator(login_required)
@class_view_decorator(permission_required('recruited_billing.add_recruitedbillingdetails', raise_exception=True))
class RecruitedBillingBudgetDetailsCreate(SuccessMessageMixin, CreateView):
	template_name = "recruited_billing_details_edit.html"
	model = RecruitedBillingDetails
	success_message = u"%(dates)s 成功申请"
	fields = [
		"dates",
		"money",
		"subject",
		"cost_sharing",
		"cost_obj",
		"cost_detail_content",
		"invoice_state",
		"payee",
	]

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(RecruitedBillingBudgetDetailsCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"待招结算与开票，费用预算明细申请"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def get_success_url(self):
		applicants = self.kwargs.get("applicants", 0)
		view_type = '1'
		self.url = reverse('approval:recruitedbilling_details_list', args=(applicants, view_type))

		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:recruitedbilling_details_add', args=(applicants))

		return self.url

	# 将登陆用户作为申请人
	def form_valid(self, form):
		try:
			applicants = self.kwargs.get("applicants", 0)
			form.instance.applicants = RecruitedBilling.objects.filter(
				id=applicants).first()  # 对应待招结算与开票申请id
			form.instance.payee = self.request.user

		except:
			traceback.print_exc()
		return super(RecruitedBillingBudgetDetailsCreate, self).form_valid(form)
