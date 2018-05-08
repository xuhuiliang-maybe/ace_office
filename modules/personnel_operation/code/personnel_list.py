# coding=utf-8
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.dict_table.models import ImproveStatus
from modules.personnel_operation.models import QualityAssurance
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE

@class_view_decorator(login_required)
@class_view_decorator(permission_required('personnel_operation.browse_qualityassurance', raise_exception=True))
class PersonnelList(ListView):
	context_object_name = "personnel_list"
	template_name = "personnel_manage_info.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.improve_status = int(self.request.GET.get("improve_status", 0))
			self.st_error_date = self.request.GET.get("st_error_date", "")
			self.et_error_date = self.request.GET.get("et_error_date", "")

			search_condition = {
				"improve_status": self.improve_status,
				"error_date__gte": self.st_error_date,
				"error_date__lte": self.et_error_date
			}
			kwargs = get_kwargs(search_condition)
			return QualityAssurance.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(PersonnelList, self).get_context_data(**kwargs)
		context["improvestatus"] = ImproveStatus.objects.all()
		context["improve_status"] = self.improve_status
		context["st_error_date"] = self.st_error_date
		context["et_error_date"] = self.et_error_date
		print context
		return context
