# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import DeleteView

from modules.contract_manage.models import *
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('contract_manage.delete_contractintern', raise_exception=True))
class ContractInternDelete(SuccessMessageMixin, DeleteView):
	model = ContractIntern
	template_name = "base/confirm_delete.html"
	success_message = u"%(name)s 删除创建"

	def get_success_url(self):
		self.url = reverse('contract:list_intern', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(ContractInternDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
