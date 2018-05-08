# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from modules.project_manage.models import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE
"""
项目基础信息
"""


@class_view_decorator(login_required)
class ProjectsList(ListView):
	context_object_name = "projects_list"
	template_name = "projects_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		# 查询条件
		self.search_name = self.request.GET.get("search_name", "")
		self.dept_ids = self.request.GET.get("dept_ids", "")
		self.dept_name = self.request.GET.get("dept_name", "")

		# 判断是否是客服部,是，只显示当前用户所属部门下信息
		self.customer_service = 0
		try:
			user_position = self.request.user.position.name  # 用户岗位
		except:
			user_position = ""
		position_list = [u"客服专员", u"客服主管", u"外包主管", u"客服经理"]
		if user_position in position_list:  # 登录用户在客服部，只能查看所在部门项目信息
			self.dept_name = self.request.user.attribution_dept
			self.customer_service = 1

		search_condition = {
			"full_name__icontains": self.search_name
		}
		if self.dept_name:
			search_condition.update({"department__name__in": self.dept_name.split(",")})
		kwargs = get_kwargs(search_condition)
		return Project.objects.filter(**kwargs)

	def get_context_data(self, **kwargs):
		url_param = self.kwargs
		project_info_type = url_param.get("project_info_type", "")  # 项目信息类型
		perm = self.request.user.has_perm('project_manage.browse_%s' % project_info_type)
		if not perm:
			raise PermissionDenied

		context = super(ProjectsList, self).get_context_data(**kwargs)
		context["dept_name"] = self.dept_name
		context["dept_ids"] = self.dept_ids
		context["search_name"] = self.search_name
		context["customer_service"] = self.customer_service
		context["project_info_type"] = project_info_type
		return context
