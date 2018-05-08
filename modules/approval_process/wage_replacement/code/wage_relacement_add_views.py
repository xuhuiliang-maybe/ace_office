# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.approval_process.wage_replacement.models import *
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('wage_replacement.add_wagereplacement', raise_exception=True))
class WageReplacementCreate(SuccessMessageMixin, CreateView):
	model = WageReplacement
	template_name = "base/document_edit.html"
	success_message = u"%(title)s 成功申请"
	fields = ["title", "note"]

	def get_success_url(self):
		self.url = reverse('approval:wage_replacement_list', args=())

		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:wage_replacement_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(WageReplacementCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"工资补发申请"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	# 将登陆用户作为申请人
	def form_valid(self, form):
		form.instance.apply_user = self.request.user
		form.instance.apply_types = "5"
		return super(WageReplacementCreate, self).form_valid(form)


@class_view_decorator(login_required)
@class_view_decorator(permission_required('wage_replacement.add_wagereplacement', raise_exception=True))
class WageReplacementDetailsCreate(SuccessMessageMixin, CreateView):
	model = WageReplacementDetails
	template_name = "wage_replacement_edit.html"
	success_message = u"%(name)s 成功申请"
	fields = ["payment_unit", "department", "project_name", "name", "identity_card_number",
		  "salary_card_number", "bank_account", "replacement_money", "cost_month", "replacement_type",
		  "replacement_explain"]

	def get_context_data(self, **kwargs):
		context = super(WageReplacementDetailsCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"工资补发申请，明细"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def get_success_url(self):
		applicants = self.kwargs.get("applicants", 0)
		view_type = '1'
		self.url = reverse('approval:wage_replacement_details_list', args=(applicants, view_type))

		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:wage_replacement_details_add', args=(applicants))

		return self.url

	# 将登陆用户作为申请人
	def form_valid(self, form):
		applicants = self.kwargs.get("applicants", 0)
		form.instance.applicants = WageReplacement.objects.filter(id=applicants).first()  # 对应申请id
		return super(WageReplacementDetailsCreate, self).form_valid(form)
