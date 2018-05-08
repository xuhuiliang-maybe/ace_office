# coding=utf-8
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.expense_manage.models import Expense
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE


@class_view_decorator(login_required)
@class_view_decorator(permission_required('expense_manage.browse_expense', raise_exception=True))
class ExpenseListView(ListView):
	context_object_name = "expense_list"
	template_name = "expense_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.dept_ids = self.request.GET.get("dept_ids", "")
			self.dept_name = self.request.GET.get("dept_name", "")
			self.project_name = self.request.GET.get("project_name", "")

			search_condition = {
				# "projectid__short_name__icontains": self.project_name,
				"projectid__full_name__icontains": self.project_name
			}
			if self.dept_name:
				search_condition.update(
					{"emplyid__project_name__department__name__in": self.dept_name.split(",")[-1]})
			kwargs = get_kwargs(search_condition)
			return Expense.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(ExpenseListView, self).get_context_data(**kwargs)
		context["dept_name"] = self.dept_name
		context["project_name"] = self.project_name
		return context
