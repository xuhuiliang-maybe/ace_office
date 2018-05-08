# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from config.conf_core import PAGINATE
from modules.dict_table.models import *
from modules.share_module.permissionMixin import class_view_decorator

dict_table_map = {
	"companysubject": CompanySubject,  # 公司主体信息
	"contracttype": ContractType,  # 合同类型信息
	"projecttype": ProjectType,  # 项目类型信息
	"progressstate": ProgressState,  # 项目目前状态信息
	"socialsecurityaccounttype": SocialSecurityAccountType,  # 社保账户类型信息
	"socialsecuritytype": SocialSecurityType,  # 社保险种信息
	"salestype": SalesType,  # 销售类型信息
	"businessinsurancecompany": BusinessInsuranceCompany,  # 商保公司信息
	"cycle": Cycle,  # 时间周期信息
	"wagegranttype": WageGrantType,  # 工资发放方式信息
	"position": Position,  # 岗位信息
	"invoicetype": InvoiceType,  # 发票类型
	"archivetype": ArchiveType,  # 档案类型
	"expensetype": ExpenseType,  # 费用类型信息
	"improvestatus": ImproveStatus,  # 改善状态信息
	"leavetype": LeaveType,  # 请假类型
	"subject": Subject,  # 科目信息
}


@class_view_decorator(login_required)
class DictTableList(ListView):
	context_object_name = "dict_table_list"
	template_name = "dict_table_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.dict_table_type = self.kwargs.get("dict_table_type", "")  # 字典表类型
			self.verbose_name = ""  # 字典表名称

			# 权限校验
			perm = self.request.user.has_perm('dict_table.browse_%s' % self.dict_table_type)
			if not perm:
				raise PermissionDenied

			dict_table_model = dict_table_map.get(self.dict_table_type)
			if dict_table_model:
				self.verbose_name = dict_table_model._meta.verbose_name
				return dict_table_model.objects.all()
			return list()
		except:
			traceback.print_exc()

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(DictTableList, self).get_context_data(**kwargs)
		context["prefix_url"] = reverse('dicttable:dict_table_list', args=(self.dict_table_type,)) + "/"
		context["dict_name"] = self.verbose_name
		return context


@class_view_decorator(login_required)
class DictTableAdd(SuccessMessageMixin, CreateView):
	template_name = "base/document_edit.html"
	success_message = u"%(name)s 成功创建"
	fields = "__all__"

	def get_queryset(self):
		self.verbose_name = ""
		self.dict_table_type = self.kwargs.get("dict_table_type", "")  # 字典表类型
		dict_table_model = dict_table_map.get(self.dict_table_type)
		self.model = dict_table_model  # 字典表对象

		if dict_table_model:  # 表名
			self.verbose_name = dict_table_model._meta.verbose_name

		# 权限校验
		perm = self.request.user.has_perm('dict_table.add_%s' % self.dict_table_type)
		if not perm:
			raise PermissionDenied

		return self

	def get_context_data(self, **kwargs):
		context = super(DictTableAdd, self).get_context_data(**kwargs)
		context["form_content"] = u"新增 " + self.verbose_name
		return context


@class_view_decorator(login_required)
class DictTableEdit(SuccessMessageMixin, UpdateView):
	template_name = "base/document_edit.html"
	success_message = u"%(name)s 成功修改"
	fields = "__all__"

	def get_queryset(self):
		self.verbose_name = ""
		self.dict_table_type = self.kwargs.get("dict_table_type", "")  # 字典表类型
		dict_table_model = dict_table_map.get(self.dict_table_type)
		self.model = dict_table_model  # 字典表对象

		if dict_table_model:  # 表名
			self.verbose_name = dict_table_model._meta.verbose_name

		# 权限校验
		perm = self.request.user.has_perm('dict_table.change_%s' % self.dict_table_type)
		if not perm:
			raise PermissionDenied

		return dict_table_model.objects

	def get_context_data(self, **kwargs):
		context = super(DictTableEdit, self).get_context_data(**kwargs)
		context["form_content"] = u"修改 " + self.verbose_name
		return context


@class_view_decorator(login_required)
class DictTableDel(DeleteView):
	template_name = "base/confirm_delete.html"

	def get_success_url(self):
		self.url = reverse('dicttable:dict_table_list', args=(self.dict_table_type,))
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(DictTableDel, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def get_queryset(self):
		self.dict_table_type = self.kwargs.get("dict_table_type", "")  # 字典表类型
		dict_table_model = dict_table_map.get(self.dict_table_type)

		# 权限校验
		perm = self.request.user.has_perm('dict_table.delete_%s' % self.dict_table_type)
		if not perm:
			raise PermissionDenied

		return dict_table_model.objects
