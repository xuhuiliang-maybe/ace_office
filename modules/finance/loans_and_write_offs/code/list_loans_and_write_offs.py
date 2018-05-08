# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.finance.loans_and_write_offs.models import LoansAndWriteOffs
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE


@class_view_decorator(login_required)
@class_view_decorator(permission_required('loans_and_write_offs.browse_loansandwriteoffs', raise_exception=True))
class LoansAndWriteOffsListView(ListView):
	context_object_name = "loans_and_write_offs_list"
	template_name = "loans_and_write_offs_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.name = self.request.GET.get("name", "")  # 姓名
			self.start_borrowing_date = self.request.GET.get("start_borrowing_date", "")  # 起始借款时间
			self.end_borrowing_date = self.request.GET.get("end_borrowing_date", "")  # 终止借款时间
			self.money = self.request.GET.get("money", "")  # 借款金额

			start_borrowing_date, end_borrowing_date = "", ""
			if self.start_borrowing_date and self.end_borrowing_date:
				start_borrowing_date = datetime.datetime.strptime(self.start_borrowing_date, "%Y/%m/%d")
				end_borrowing_date = datetime.datetime.strptime(self.end_borrowing_date, "%Y/%m/%d")

			search_condition = {
				"loan__apply_user__first_name__icontains": self.name,
				"loan__money": self.money,
				"loan__borrowing_date__gte": start_borrowing_date,
				"loan__borrowing_date__lte": end_borrowing_date,
			}
			kwargs = get_kwargs(search_condition)
			return LoansAndWriteOffs.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(LoansAndWriteOffsListView, self).get_context_data(**kwargs)
		context["name"] = self.name
		context["start_borrowing_date"] = self.start_borrowing_date
		context["end_borrowing_date"] = self.end_borrowing_date
		context["money"] = self.money
		return context
