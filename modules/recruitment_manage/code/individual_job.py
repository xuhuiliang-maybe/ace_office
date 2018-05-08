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
个人招聘
"""


@class_view_decorator(login_required)
@class_view_decorator(permission_required('admin_account.browse_individual_job', raise_exception=True))
class IndividualJobListView(ListView):
	context_object_name = "employee_list"
	template_name = "individual_job_info.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.project_name = self.request.GET.get("project_name", "")  # 项目名称
			self.dept_name = self.request.GET.get("dept_name", "")  # 服务部门
			self.dept_ids = self.request.GET.get("dept_ids", "")  # 服务部门id
			self.name = self.request.GET.get("name", "")  # 员工姓名
			self.recruitment_attache = self.request.GET.get("recruitment_attache", "")  # 招聘人员
			self.query_month = self.request.GET.get("query_month", "")  # 查询月度
			self.channel = self.request.GET.get("channel", "")  # 招聘渠道

			# 普通用户，只能查看自己招聘的员工
			search_condition = {
				"recruitment_attache": self.request.user,  # 招聘人员
				"project_name__full_name__icontains": self.project_name,  # 项目名称
				"name__icontains": self.name,  # 员工姓名
				"recruitment_channel": self.channel,
			}
			if not self.query_month:
				# 默认显示当月入职
				search_condition.update({
					"entry_date__year": timezone.now().year,
					"entry_date__month": timezone.now().month
				})
			else:
				# 按查询月份筛选
				query_month = date_formater(self.query_month, "%Y/%m/%d")
				search_condition.update(
					{
						"entry_date__year": query_month.year,
						"entry_date__month": query_month.month
					})

			# 登陆用户是部门负责人，可查看所在部门下所有招聘信息
			if self.request.user.dept_head:
				search_condition.update(
					{"project_name__department__name": self.request.user.attribution_dept}
				)  # 部门负责人，可查看所在部门下所有人

			# 超级管理员可查看所有招聘记录
			if self.request.user.is_superuser:
				search_condition["project_name__department__name"] = ""  # 删除指定部门条件
				if self.dept_name:
					search_condition.update(
						{"project_name__department__name__in": self.dept_name.split(",")})

			if self.request.user.is_superuser or self.request.user.dept_head:
				search_condition["recruitment_attache"] = ""  # 删除招聘人为当前用户条件
				search_condition.update(
					{"recruitment_attache__first_name__icontains": self.recruitment_attache}
				)  # 对招聘人做筛选

			kwargs = get_kwargs(search_condition)
			return Employee.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(IndividualJobListView, self).get_context_data(**kwargs)
		context["project_name"] = self.project_name
		context["dept_name"] = self.dept_name
		context["dept_ids"] = self.dept_ids
		context["name"] = self.name
		context["recruitment_attache"] = self.recruitment_attache
		context["query_month"] = self.query_month
		context["channel"] = self.channel
		context["list_channel"] = RECRUITMENTCHANNEL_CHOICES
		return context
