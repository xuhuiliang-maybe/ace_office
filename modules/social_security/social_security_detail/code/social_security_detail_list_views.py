# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.views.generic import ListView

from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from modules.social_security.social_security_detail.models import SocialSecurityDetail
from config.conf_core import PAGINATE

@class_view_decorator(login_required)
@class_view_decorator(permission_required('increase_info.browse_social_security_detail', raise_exception=True))
class SocialSecurityDetailListView(ListView):
	context_object_name = "social_security_detail_list"
	template_name = "social_security_detail_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			# 查询条件
			self.project_name = self.request.GET.get("project_name", "")  # 项目名称
			self.department = self.request.GET.get("department", "")  # 服务部门
			self.identity_card_number = self.request.GET.get("identity_card_number", "")  # 身份证号
			self.name = self.request.GET.get("name", "")  # 姓名
			self.insured_month = self.request.GET.get("insured_month", "")  # 参保月份

			if self.insured_month:
				insured_month = date_formater(self.insured_month, "%Y/%m/%d")
				insured_month_year = insured_month.year
				insured_month_month = insured_month.month
			else:
				insured_month_year = timezone.now().year
				insured_month_month = timezone.now().month

			search_condition = {
				"project_name__full_name__icontains": self.project_name,
				"identity_card_number__icontains": self.identity_card_number,
				"name__icontains": self.name,
				"insured_month__year": insured_month_year,
				"insured_month__month": insured_month_month,
			}

			# 判断是否是客服部,是，只显示当前用户所属部门下信息
			self.customer_service = 0
			try:
				user_position = self.request.user.position.name  # 用户岗位
			except:
				user_position = ""
			position_list = [u"客服专员", u"客服主管", u"外包主管", u"客服经理"]
			if user_position in position_list:  # 登录用户在客服部，只能查看所在部门项目信息
				self.department = self.request.user.attribution_dept
				self.customer_service = 1

			if self.department:
				search_condition.update(
					{"project_name__department__name__in": self.department.split(",")})
			kwargs = get_kwargs(search_condition)
			return SocialSecurityDetail.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(SocialSecurityDetailListView, self).get_context_data(**kwargs)
		context["project_name"] = self.project_name
		context["department"] = self.department
		context["identity_card_number"] = self.identity_card_number
		context["name"] = self.name
		context["insured_month"] = self.insured_month
		context["customer_service"] = self.customer_service
		context["export_url"] = reverse('social_security_detail:social_security_detail_export')
		return context
