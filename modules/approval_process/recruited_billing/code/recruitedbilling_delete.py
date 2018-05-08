# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import DeleteView

from modules.approval_process.recruited_billing.models import *
from modules.share_module.check_decorator import check_is_approval
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('recruited_billing.delete_recruitedbilling', raise_exception=True))
@class_view_decorator(check_is_approval)
class RecruitedBillingDelete(SuccessMessageMixin, DeleteView):
	model = RecruitedBilling
	template_name = "base/confirm_delete.html"
	success_message = u"%(title)s 删除创建"

	def get_success_url(self):
		self.url = reverse('approval:recruitedbilling_list')
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(RecruitedBillingDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context


@class_view_decorator(login_required)
@class_view_decorator(permission_required('recruited_billing.delete_recruitedbillingdetails', raise_exception=True))
@class_view_decorator(check_is_approval)
class RecruitedBillingDetailsDelete(SuccessMessageMixin, DeleteView):
	model = RecruitedBillingDetails
	template_name = "base/confirm_delete.html"
	success_message = u"%(dates)s 删除创建"

	def get_object(self, queryset=None):
		return super(RecruitedBillingDetailsDelete, self).get_object()

	def get_success_url(self):
		applicants = self.kwargs.get("applicants", 0)
		self.url = reverse('approval:recruitedbilling_details_list', args=(applicants, "1"))
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(RecruitedBillingDetailsDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context