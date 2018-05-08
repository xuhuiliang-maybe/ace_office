# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.employee_management.employee_info.models import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE


@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.browse_archive', raise_exception=True))
class ArchiveList(ListView):
	context_object_name = "archive_list"
	template_name = "archive_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		# 查询参数
		self.name = self.request.GET.get("name", "")  # 姓名
		self.identity_card_number = self.request.GET.get("identity_card_number", "")  # 身份证号
		self.project_name = self.request.GET.get("project_name", "")  # 项目名称
		self.status = self.request.GET.get("status", "")  # 目前状态
		self.issue = self.request.GET.get("issue", "")  # 是否发出
		self.receive = self.request.GET.get("receive", "")  # 是否收到

		search_condition = {
			"employee_id__name__icontains": self.name,
			"employee_id__identity_card_number__icontains": self.identity_card_number,
			"employee_id__project_name__full_name__icontains": self.project_name,
			"employee_id__status": self.status,
			"issue": self.issue,
			"receive": self.receive
		}
		kwargs = get_kwargs(search_condition)

		return Archive.objects.filter(**kwargs)

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(ArchiveList, self).get_context_data(**kwargs)
		context["name"] = self.name
		context["identity_card_number"] = self.identity_card_number
		context["project_name"] = self.project_name
		context["status"] = self.status
		context["list_status"] = IS_WORK
		context["issue"] = self.issue
		context["receive"] = self.receive
		context["list_issue_status"] = ISSUE_STATUS
		return context
