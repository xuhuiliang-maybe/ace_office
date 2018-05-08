# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import DeleteView

from modules.finance.arrival_and_billing.models import *
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('arrival_and_billing.delete_arrivalandbilling', raise_exception=True))
class ArrivalAndBillingDelete(SuccessMessageMixin, DeleteView):
	model = ArrivalAndBilling
	template_name = "base/confirm_delete.html"
	success_message = u"%(project_name)s 删除创建"

	def get_success_url(self):
		self.url = reverse('finance:arrival_and_billing:list_arrivalandbilling', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(ArrivalAndBillingDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context


@class_view_decorator(login_required)
class CreditedDetailsDelete(SuccessMessageMixin, DeleteView):
	model = CreditedDetails
	template_name = "base/confirm_delete.html"
	success_message = u"%(credited_amount)s 删除创建"

	# 重定向url
	def get_success_url(self):
		self.arrivalandbilling = self.kwargs.get("arrivalandbilling", "")
		self.url = reverse('finance:arrival_and_billing:list_crediteddetails', args=(self.arrivalandbilling))

		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(CreditedDetailsDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context


@class_view_decorator(login_required)
class BillingDetailsDelete(SuccessMessageMixin, DeleteView):
	model = BillingDetails
	template_name = "base/confirm_delete.html"
	success_message = u"%(credited_amount)s 删除创建"

	# 重定向url
	def get_success_url(self):
		self.arrivalandbilling = self.kwargs.get("arrivalandbilling", "")
		self.url = reverse('finance:arrival_and_billing:list_billingdetails', args=(self.arrivalandbilling))
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(BillingDetailsDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
