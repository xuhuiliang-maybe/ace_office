# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils import timezone
from django.views.generic import ListView

from modules.contract_manage.models import *
from modules.share_module.check_decorator import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE


@class_view_decorator(login_required)
@class_view_decorator(permission_required('contract_manage.browse_contractpreviewcode', raise_exception=True))
class ContractPreviewCodeListView(ListView):
	context_object_name = "preview_code_list"
	template_name = "preview_code_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.contract_type = self.request.GET.get("contract_type", "")  # 合同类型
			self.status = self.request.GET.get("status", "")  # 状态

			search_condition = {
				"contract_type": self.contract_type,
			}
			if self.status == "1":  # 有效
				search_condition.update({"end_time__gt": timezone.now()})
			elif self.status == "2":
				search_condition.update({"end_time__lt": timezone.now()})

			kwargs = get_kwargs(search_condition)
			return ContractPreviewCode.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(ContractPreviewCodeListView, self).get_context_data(**kwargs)
		context["contract_type"] = self.contract_type
		context["status"] = self.status
		context["list_contract_type"] = CONTRACT_TYPE
		return context


@class_view_decorator(check_employee)  # 校验是否有此员工
class ContractTypeListView(ListView):
	context_object_name = "contract_list"
	template_name = "all_contract_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		self.active = ""
		self.send = ""
		self.outsourc = ""
		self.intern = ""
		self.service = ""
		self.hourly = ""
		try:
			self.active = self.request.GET.get("active", "")  # 选中某类型合同
			self.name = self.request.GET.get("name")
			self.identity_card_number = self.request.GET.get("identity_card_number")

			return_list_dict = dict()

			send_list = ContractSend.objects.filter(name=self.name, identity_card_number=self.identity_card_number)
			if send_list.exists():
				self.send = "1"  # 显示标签
				return_list_dict.update({"1": send_list})
				if not self.active:
					self.active = "1"

			outsourc_list = ContractOutsourc.objects.filter(name=self.name, identity_card_number=self.identity_card_number)
			if outsourc_list.exists():
				self.outsourc = "2"  # 显示标签
				return_list_dict.update({"2": outsourc_list})
				if not self.active:
					self.active = "2"

			intern_list = ContractIntern.objects.filter(name=self.name, identity_card_number=self.identity_card_number)
			if intern_list.exists():
				self.intern = "3"  # 显示标签
				return_list_dict.update({"3": intern_list})
				if not self.active:
					self.active = "3"

			service_list = ContractService.objects.filter(name=self.name, identity_card_number=self.identity_card_number)
			if service_list.exists():
				self.service = "4"  # 显示标签
				return_list_dict.update({"4": service_list})
				if not self.active:
					self.active = "4"

			hourly_list = ContractHourly.objects.filter(name=self.name, identity_card_number=self.identity_card_number)
			if hourly_list.exists():
				self.hourly = "5"  # 显示标签
				return_list_dict.update({"5": hourly_list})
				if not self.active:
					self.active = "5"

			result = return_list_dict.get(self.active, [])
			if not result:
				self.active = ""
			return result
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(ContractTypeListView, self).get_context_data(**kwargs)
		context["name"] = self.name
		context["identity_card_number"] = self.identity_card_number
		context["active"] = self.active
		context["send"] = self.send
		context["outsourc"] = self.outsourc
		context["intern"] = self.intern
		context["service"] = self.service
		context["hourly"] = self.hourly
		return context
