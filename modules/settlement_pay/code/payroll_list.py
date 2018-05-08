# coding=utf-8
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.settlement_pay.models import Payroll
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE

@class_view_decorator(login_required)
@class_view_decorator(permission_required('settlement_pay.browse_payroll', raise_exception=True))
class PayrollListView(ListView):
	context_object_name = "payroll_list"
	template_name = "payroll_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.pay_month = self.request.GET.get("pay_month", "")
			search_condition = {"pay_month": self.pay_month}
			kwargs = get_kwargs(search_condition)
			return Payroll.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	# 增加返回参数
	def get_context_data(self, **kwargs):
		try:
			context = super(PayrollListView, self).get_context_data(**kwargs)
			context["pay_month"] = self.pay_month
			return context
		except:
			traceback.print_exc()
