# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import DeleteView

from modules.approval_process.wage_replacement.models import *
from modules.share_module.check_decorator import check_is_approval
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('wage_replacement.delete_wagereplacement', raise_exception=True))
@class_view_decorator(check_is_approval)
class WageReplacementDelete(SuccessMessageMixin, DeleteView):
	model = WageReplacement
	template_name = "base/confirm_delete.html"
	success_message = u"%(title)s 删除创建"

	def get_success_url(self):
		self.url = reverse('approval:wage_replacement_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(WageReplacementDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context


@class_view_decorator(login_required)
@class_view_decorator(permission_required('wage_replacement.delete_wagereplacement', raise_exception=True))
@class_view_decorator(check_is_approval)
class WageReplacementDetailsDelete(SuccessMessageMixin, DeleteView):
	model = WageReplacementDetails
	template_name = "base/confirm_delete.html"
	success_message = u"%(name)s 删除创建"

	def get_success_url(self):
		applicants = self.kwargs.get("applicants", 0)
		self.url = reverse('approval:wage_replacement_details_list', args=(applicants, "1"))

		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		return self.url

	def get_object(self, queryset=None):
		return super(WageReplacementDetailsDelete, self).get_object()

	def get_context_data(self, **kwargs):
		context = super(WageReplacementDetailsDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
