# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.views.generic import ListView

from modules.approval_process.leave.models import Leave
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE


@class_view_decorator(login_required)
@class_view_decorator(permission_required('leave.browse_leave', raise_exception=True))
class LeaveListView(ListView):
	context_object_name = "leave_list"
	template_name = "all_apply_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.pk = self.kwargs.get("pk", "")  # 用于待审批查看
			self.view_type = self.kwargs.get("view_type", "1")
			self.title = self.request.GET.get("title", "")
			self.status = self.request.GET.get("status", "")
			self.month = self.request.GET.get("month", "")  # 月份
			self.dept_name = self.request.GET.get("dept_name", "")  # 部门名称

			created_year = ""
			created_month = ""
			if self.month:
				created_date = date_formater(self.month, "%Y/%m/%d")
				created_year = created_date.year
				created_month = created_date.month

			search_condition = {
				"pk": self.pk,
				"title__icontains": self.title,
				"status": self.status,
				"created__year": created_year,
				"created__month": created_month,
				"apply_user__attribution_dept__icontains": self.dept_name,
			}
			if not self.request.user.is_superuser and self.view_type == "1":
				search_condition.update({"apply_user": self.request.user})

			kwargs = get_kwargs(search_condition)
			return Leave.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(LeaveListView, self).get_context_data(**kwargs)
		context["title"] = self.title  # 标题回显
		context["status"] = self.status  # 审核状态回显
		context["month"] = self.month  # 申请月份
		context["dept_name"] = self.dept_name  # 部门
		context["add_url"] = reverse('approval:leave_add')  # 新增url
		context["apply_type"] = "leave"  # 申请类型
		# 查看方式，# 1:由明细表返回，申请页面带查询条件，2：由待审批超链进去，不带查询条件
		context["view_type"] = self.view_type
		return context
