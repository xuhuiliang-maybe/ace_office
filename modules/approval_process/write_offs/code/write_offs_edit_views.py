# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.approval_process.write_offs.models import *
from modules.share_module.check_decorator import check_is_approval
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('write_offs.change_writeoffs', raise_exception=True))
@class_view_decorator(check_is_approval)
class WriteOffsUpdate(SuccessMessageMixin, UpdateView):
	model = WriteOffs
	form_class = WriteOffsForm
	template_name = "base/document_edit.html"
	success_message = u"%(title)s 成功修改"

	def get_success_url(self):
		self.url = reverse('approval:write_offs_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:write_offs_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(WriteOffsUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改报销与销账"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	# 将登陆用户作为申请人
	def form_valid(self, form):

		# 报销/销账总额 = 报销/销账明细中金额总和，本字段下方有报销/销账明细表
		writeoffs_total_sum = WriteOffsDetails.objects.filter(applicants=form.instance).aggregate(Sum('money'))
		money_sum = writeoffs_total_sum["money__sum"]
		if money_sum:
			writeoffs_total = money_sum
		else:
			writeoffs_total = 0
		form.instance.writeoffs_total = writeoffs_total  # 默认0

		# 差额
		borrow_imprest = self.request.POST.get("borrow_imprest", "")  # 已借备用金
		form.instance.difference = int(borrow_imprest) - writeoffs_total

		return super(WriteOffsUpdate, self).form_valid(form)


@class_view_decorator(login_required)
@class_view_decorator(permission_required('write_offs.change_writeoffs', raise_exception=True))
@class_view_decorator(check_is_approval)
class WriteOffsDetailsUpdate(SuccessMessageMixin, UpdateView):
	model = WriteOffsDetails
	template_name = "base/document_edit.html"
	success_message = u"%(date_range)s 成功修改"
	fields = ["date_range", "money", "subject", "department", "project_name", "cost_sharing", "cost_detail",
		  "invoice_situation", "remark"]

	def get_context_data(self, **kwargs):
		context = super(WriteOffsDetailsUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改报销与销账，明细"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def get_success_url(self):
		applicants = self.kwargs.get("applicants", 0)
		view_type = '1'
		self.url = reverse('approval:write_offs_details_list', args=(applicants, view_type))

		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:write_offs_details_add', args=(applicants))
		return self.url

	def form_valid(self, form):
		return super(WriteOffsDetailsUpdate, self).form_valid(form)
