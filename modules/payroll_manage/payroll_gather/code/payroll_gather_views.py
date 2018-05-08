# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.dict_table.models import *
from modules.payroll_manage.payroll_detail.models import PayrollDetail
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE

@class_view_decorator(login_required)
@class_view_decorator(permission_required('payroll_gather.browse_payrollgather', raise_exception=True))
class PayrollGatherListView(ListView):
	context_object_name = "payroll_detail_list"
	template_name = "payroll_gather_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.project_name = self.request.GET.get("project_name", "")  # 项目名称
			self.settle_accounts_month = self.request.GET.get("settle_accounts_month", "")  # 结算月份
			self.service_company = int(self.request.GET.get("service_company", 0))

			if self.settle_accounts_month:
				settle_accounts_month = date_formater(self.settle_accounts_month, "%Y/%m/%d")
				settle_accounts_month_year = settle_accounts_month.year
				settle_accounts_month_month = settle_accounts_month.month
			else:
				settle_accounts_month_year = timezone.now().year
				settle_accounts_month_month = timezone.now().month

			search_condition = {
				"project_name__full_name__icontains": self.project_name,
				"project_name__company_subject": self.service_company,
				"settle_accounts_month__year": settle_accounts_month_year,
				"settle_accounts_month__month": settle_accounts_month_month,
			}

			kwargs = get_kwargs(search_condition)
			return PayrollDetail.objects.values("project_name").order_by("project_name").distinct().filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(PayrollGatherListView, self).get_context_data(**kwargs)
		context["project_name"] = self.project_name
		context["settle_accounts_month"] = self.settle_accounts_month
		context["service_company"] = self.service_company
		context["company_subject_list"] = CompanySubject.objects.all()
		return context
