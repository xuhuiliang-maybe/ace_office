# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.approval_process.recruited_billing.models import *
from modules.share_module.check_decorator import check_is_approval
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('recruited_billing.change_recruitedbilling', raise_exception=True))
@class_view_decorator(check_is_approval)
class RecruitedBillingUpdate(SuccessMessageMixin, UpdateView):
	template_name = "recruited_billing_edit.html"
	model = RecruitedBilling
	success_message = u"%(title)s 成功修改"
	fields = ["title", "note", "project_name", "billing_month", "settlement_amount", "is_billing", "content"]

	def get_context_data(self, **kwargs):
		context = super(RecruitedBillingUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改 待招结算与销账"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def get_success_url(self):
		self.url = reverse('approval:recruitedbilling_list')
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:recruitedbilling_add')
		return self.url


@class_view_decorator(login_required)
@class_view_decorator(permission_required('recruited_billing.change_recruitedbillingdetails', raise_exception=True))
@class_view_decorator(check_is_approval)
class RecruitedBillingDetailsUpdate(SuccessMessageMixin, UpdateView):
	model = RecruitedBillingDetails
	template_name = "base/document_edit.html"
	success_message = u"%(dates)s 成功修改"
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

	def get_context_data(self, **kwargs):
		context = super(RecruitedBillingDetailsUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改 待招结算与销账，报销/销账明细"
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

	def form_valid(self, form):
		return super(RecruitedBillingDetailsUpdate, self).form_valid(form)
