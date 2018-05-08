# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from modules.system.models import *
from config.conf_core import PAGINATE

@class_view_decorator(login_required)
@class_view_decorator(permission_required('system.browse_databackup', raise_exception=True))
class BackupListView(ListView):
	context_object_name = "system_backup_list"
	template_name = "system_backup_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.bak_starttime = self.request.GET.get("bak_starttime", "")
			self.bak_endtime = self.request.GET.get("bak_endtime", "")
			self.status = self.request.GET.get("status", "")

			search_condition = {"starttime__gte": self.bak_starttime,
					    "starttime__lte": self.bak_endtime,
					    "status": self.status}

			kwargs = get_kwargs(search_condition)
			return DataBackup.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(BackupListView, self).get_context_data(**kwargs)
		context["bak_starttime"] = self.bak_starttime
		context["bak_endtime"] = self.bak_endtime
		context["status"] = self.status
		context["list_status"] = STATUS_CHOICES
		return context
