# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from modules.social_security.increase_info.models import Increase
from config.conf_core import PAGINATE

@class_view_decorator(login_required)
@class_view_decorator(permission_required('increase_info.browse_increase', raise_exception=True))
class IncreaseListView(ListView):
	context_object_name = "increase_list"
	template_name = "increase_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			# 查询条件
			self.dept_name = self.request.GET.get("dept_name", "")  # 部门名称
			self.dept_ids = self.request.GET.get("dept_ids", "")
			self.name = self.request.GET.get("name", "")  # 姓名
			self.month = self.request.GET.get("month", "")  # 月份

			increaseyear = ""
			increasemonth = ""
			if self.month:
				increasedate = date_formater(self.month, "%Y/%m/%d")
				increaseyear = increasedate.year
				increasemonth = increasedate.month

			search_condition = {
				"emplyid__name__icontains": self.name,
				"emplyid__social_insurance_increase_date__year": increaseyear,
				"emplyid__social_insurance_increase_date__month": increasemonth,
			}

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

			if self.dept_name:
				search_condition.update({"emplyid__project_name__department__name__in": self.dept_name.split(",")})
			kwargs = get_kwargs(search_condition)
			return Increase.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(IncreaseListView, self).get_context_data(**kwargs)
		context["dept_name"] = self.dept_name
		context["dept_ids"] = self.dept_ids
		context["name"] = self.name
		context["month"] = self.month
		context["customer_service"] = self.customer_service
		return context
