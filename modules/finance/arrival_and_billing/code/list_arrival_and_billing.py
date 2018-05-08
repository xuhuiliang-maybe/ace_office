# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.finance.arrival_and_billing.models import *
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE


@class_view_decorator(login_required)
@class_view_decorator(permission_required('arrival_and_billing.browse_arrivalandbilling', raise_exception=True))
class ArrivalAndBillingListView(ListView):
	context_object_name = "arrival_and_billing_list"
	template_name = "arrival_and_billing_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.settlement_date = self.request.GET.get("settlement_date", "")  # 结算月份

			settlement_date_year = ""
			settlement_date_month = ""
			if self.settlement_date:
				settlement_date_date = date_formater(self.settlement_date, "%Y/%m/%d")
				settlement_date_year = settlement_date_date.year
				settlement_date_month = settlement_date_date.month

			search_condition = {
				"settlement_date__year": settlement_date_year,
				"settlement_date__month": settlement_date_month,
			}

			kwargs = get_kwargs(search_condition)
			return ArrivalAndBilling.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(ArrivalAndBillingListView, self).get_context_data(**kwargs)
		context["settlement_date"] = self.settlement_date
		return context


@class_view_decorator(login_required)
class CreditedDetailsListView(ListView):
	context_object_name = "credited_details_list"
	template_name = "credited_details_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.arrivalandbilling = self.kwargs.get("arrivalandbilling", "")
			self.credited_date = self.request.GET.get("credited_date", "")  # 到账时间

			credited_date_year = ""
			credited_date_month = ""
			if self.credited_date:
				credited_date = date_formater(self.credited_date, "%Y/%m/%d")
				credited_date_year = credited_date.year
				credited_date_month = credited_date.month

			search_condition = {
				"credited_date__year": credited_date_year,
				"credited_date__month": credited_date_month,
				"arrival": self.arrivalandbilling,
			}

			kwargs = get_kwargs(search_condition)
			return CreditedDetails.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(CreditedDetailsListView, self).get_context_data(**kwargs)
		context["credited_date"] = self.credited_date
		context["arrivalandbilling"] = self.arrivalandbilling
		return context


@class_view_decorator(login_required)
class BillingDetailsListView(ListView):
	context_object_name = "billing_details_list"
	template_name = "billing_details_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.arrivalandbilling = self.kwargs.get("arrivalandbilling", "")
			self.billing_date = self.request.GET.get("billing_date", "")  # 开票时间

			billing_date_year = ""
			billing_date_month = ""
			if self.billing_date:
				billing_date = date_formater(self.billing_date, "%Y/%m/%d")
				billing_date_year = billing_date.year
				billing_date_month = billing_date.month

			search_condition = {
				"billing_date__year": billing_date_year,
				"billing_date__month": billing_date_month,
				"billing": self.arrivalandbilling,
			}

			kwargs = get_kwargs(search_condition)
			return BillingDetails.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(BillingDetailsListView, self).get_context_data(**kwargs)
		context["billing_date"] = self.billing_date
		context["arrivalandbilling"] = self.arrivalandbilling
		return context
