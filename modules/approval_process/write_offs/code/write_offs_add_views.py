# coding=utf-8
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.approval_process.write_offs.models import *
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('write_offs.add_writeoffs', raise_exception=True))
class WriteOffsCreate(SuccessMessageMixin, CreateView):
	template_name = "base/document_edit.html"
	success_message = u"%(title)s 成功申请"
	form_class = WriteOffsForm

	def get_success_url(self):
		self.url = reverse('approval:write_offs_list', args=())
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:write_offs_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(WriteOffsCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"报销与销账"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	# 将登陆用户作为申请人
	def form_valid(self, form):
		form.instance.apply_user = self.request.user
		form.instance.apply_types = "3"

		# 报销/销账总额
		writeoffs_total = 0
		form.instance.writeoffs_total = writeoffs_total  # 新增，默认0

		# 差额
		borrow_imprest = self.request.POST.get("borrow_imprest", "")  # 已借备用金
		form.instance.difference = int(borrow_imprest) - writeoffs_total

		return super(WriteOffsCreate, self).form_valid(form)


@class_view_decorator(login_required)
@class_view_decorator(permission_required('write_offs.add_writeoffs', raise_exception=True))
class WriteOffsDetailsCreate(SuccessMessageMixin, CreateView):
	template_name = "write_offs_details_edit.html"
	model = WriteOffsDetails
	success_message = u"%(date_range)s 成功申请"
	fields = ["date_range", "money", "subject", "department", "project_name", "cost_sharing", "cost_detail",
		  "invoice_situation", "remark"]

	def get_context_data(self, **kwargs):
		context = super(WriteOffsDetailsCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"报销与销账，明细"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def get_success_url(self):
		applicants = self.kwargs.get("applicants", 0)
		view_type = '1'
		self.url = reverse('approval:write_offs_details_list', args=(applicants, view_type))

		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:write_offs_details_add', args=(applicants))

		return self.url

	# 将登陆用户作为申请人
	def form_valid(self, form):
		cost_sharing = self.request.POST.get("cost_sharing", "")
		project_name = self.request.POST.get("project_name", "")
		if cost_sharing == "1":  # 分摊方式为项目分摊，1，费用项目必填
			if not project_name:
				messages.warning(self.request, u"费用项目信息，必填！")
				return super(WriteOffsDetailsCreate, self).form_invalid(form)

		applicants = self.kwargs.get("applicants", 0)
		form.instance.applicants = WriteOffs.objects.filter(id=applicants).first()  # 对应申请id
		form.instance.payee = self.request.user  # 领款人

		return super(WriteOffsDetailsCreate, self).form_valid(form)
