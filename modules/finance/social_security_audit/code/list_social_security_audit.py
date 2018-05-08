# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.finance.social_security_audit.models import *
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE


@class_view_decorator(login_required)
@class_view_decorator(permission_required('social_security_audit.browse_socialsecurityaudit', raise_exception=True))
class SocialSecurityAuditListView(ListView):
	context_object_name = "social_security_audit_list"
	template_name = "social_security_audit_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.social_security_date = self.request.GET.get("social_security_date", "")  # 社保月份
			self.name = self.request.GET.get("name", "")  # 姓名
			self.identity_card_number = self.request.GET.get("identity_card_number", "")  # 身份证号
			self.job_dept = self.request.GET.get("job_dept", "")  # 部门名称
			self.project_name = self.request.GET.get("project_name", "")  # 项目名称
			self.social_security_balance = self.request.GET.get("social_security_balance", "")  # 社保平衡
			self.provident_fund_balance = self.request.GET.get("provident_fund_balance", "")  # 公积金平衡

			if self.social_security_date:
				social_security_date = date_formater(self.social_security_date, "%Y/%m/%d")
				social_security_date_year = social_security_date.year
				social_security_date_month = social_security_date.month
			else:
				social_security_date_year = timezone.now().year
				social_security_date_month = timezone.now().month
				self.social_security_date = timezone.now().strftime("%Y/%m/%d")

			search_condition = {
				"social_security_date__year": social_security_date_year,
				"social_security_date__month": social_security_date_month,
				"name__icontains": self.name,
				"identity_card_number__icontains": self.identity_card_number,
				"employee__job_dept__icontains": self.job_dept,
				"employee__project_name__full_name__icontains": self.project_name,
				"social_security_balance": self.social_security_balance,
				"provident_fund_balance": self.provident_fund_balance,
			}

			kwargs = get_kwargs(search_condition)
			return SocialSecurityAudit.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(SocialSecurityAuditListView, self).get_context_data(**kwargs)
		context["social_security_date"] = self.social_security_date
		context["name"] = self.name
		context["identity_card_number"] = self.identity_card_number
		context["job_dept"] = self.job_dept
		context["project_name"] = self.project_name
		context["social_security_balance"] = self.social_security_balance
		context["provident_fund_balance"] = self.provident_fund_balance

		context["list_social_security_balance"] = SOCIAL_SECURITY_BALANCE
		context["list_provident_fund_balance"] = SOCIAL_SECURITY_BALANCE
		return context
