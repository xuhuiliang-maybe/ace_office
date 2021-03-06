# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.contract_manage.hourly.hourly_forms import ContractHourlyForm
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('contract_manage.add_contracthourly', raise_exception=True))
class ContractHourlyCreate(SuccessMessageMixin, CreateView):
	form_class = ContractHourlyForm
	template_name = "contract_edit.html"
	success_message = u"%(name)s 创建成功"

	def get_context_data(self, **kwargs):
		context = super(ContractHourlyCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"合同签订-小时工"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def get_success_url(self):
		self.url = reverse('contract:list_hourly', args=())
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('contract:add_hourly')
		return self.url

	def form_valid(self, form):
		return super(ContractHourlyCreate, self).form_valid(form)
