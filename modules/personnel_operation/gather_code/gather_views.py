# coding=utf-8
import calendar
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.personnel_operation.models import QualityAssurance
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE

@class_view_decorator(login_required)
@class_view_decorator(permission_required('personnel_operation.browse_qualityassurance_gather', raise_exception=True))
class GatherList(ListView):
	context_object_name = "gather_list"
	template_name = "operation_gather_info.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		self.dept_name = self.request.GET.get("dept_name", "")
		self.dept_ids = self.request.GET.get("dept_ids", "")
		self.query_month = self.request.GET.get("query_month", "")

		month_start_day = ""
		month_end_day = ""
		if self.query_month:
			month_start_day = datetime.datetime.strptime(self.query_month, "%Y/%m/%d").date()
			end_day = calendar.monthrange(month_start_day.year, month_start_day.month)
			month_end_day = datetime.date(month_start_day.year, month_start_day.month, end_day[1])

		search_condition = {
			"error_date__gte": month_start_day,
			"error_date__lte": month_end_day
		}
		if self.dept_name:
			search_condition.update({"department__name__icontains": self.dept_name.split(",")})
		kwargs = get_kwargs(search_condition)
		return QualityAssurance.objects.values("project_id").order_by("project_id").distinct().filter(**kwargs)

	def get_context_data(self, **kwargs):
		context = super(GatherList, self).get_context_data(**kwargs)
		context["dept_name"] = self.dept_name
		context["dept_ids"] = self.dept_ids
		context["query_month"] = self.query_month
		return context
