# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.contract_manage.models import *
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE


@class_view_decorator(login_required)
@class_view_decorator(permission_required('contract_manage.browse_contractsend', raise_exception=True))
class ContractSendListView(ListView):
	context_object_name = "contract_send_list"
	template_name = "send_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.project_name = self.request.GET.get("project_name", "")  # 项目名称

			search_condition = {
				"project_name__full_name__icontains": self.project_name,
			}
			kwargs = get_kwargs(search_condition)
			return ContractSend.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(ContractSendListView, self).get_context_data(**kwargs)
		context["project_name"] = self.project_name  # 项目名称
		return context
