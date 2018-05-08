# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.employee_management.employee_info.models import *
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE
"""
当月入职招聘明细
"""


@class_view_decorator(login_required)
@class_view_decorator(permission_required('admin_account.browse_month_entry_job_details', raise_exception=True))
class MonthEntryJobDetailsListView(ListView):
	context_object_name = "employee_list"
	template_name = "month_entry_job_details.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.project_name = self.request.GET.get("project_name", "")  # 项目名称
			self.dept_name = self.request.GET.get("dept_name", "")  # 服务部门
			self.dept_ids = self.request.GET.get("dept_ids", "")  # 服务部门id
			self.recruitment_attache = self.request.GET.get("recruitment_attache", "")  # 招聘人员
			self.channel = self.request.GET.get("channel", "")  # 招聘渠道
			self.entry_date = self.request.GET.get("entry_date", "")  # 入职月份

			search_condition = {
				"project_name__full_name__icontains": self.project_name,  # 项目名称
				"recruitment_attache__first_name__icontains": self.recruitment_attache,  # 招聘人员
				"recruitment_channel": self.channel,
			}
			if self.dept_name:
				search_condition.update(
					{"project_name__department__name__in": self.dept_name.split(",")})
			if not self.entry_date:
				# 默认查询入职时间为当月
				search_condition.update(
					{
						"entry_date__year": timezone.now().year,
						"entry_date__month": timezone.now().month
					})
			else:
				entry_date_datetime = date_formater(self.entry_date, "%Y/%m/%d")
				search_condition.update(
					{
						"entry_date__year": entry_date_datetime.year,
						"entry_date__month": entry_date_datetime.month
					})

			kwargs = get_kwargs(search_condition)

			return Employee.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(MonthEntryJobDetailsListView, self).get_context_data(**kwargs)
		context["project_name"] = self.project_name
		context["dept_name"] = self.dept_name
		context["dept_ids"] = self.dept_ids
		context["recruitment_attache"] = self.recruitment_attache
		context["channel"] = self.channel
		context["list_channel"] = RECRUITMENTCHANNEL_CHOICES
		context["entry_date"] = self.entry_date
		return context
