# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.approval_process.demand_turnover.models import DemandTurnover
from modules.share_module.check_decorator import check_is_approval
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('demand_turnover.change_demandturnover', raise_exception=True))
@class_view_decorator(check_is_approval)
class DemandTurnoverUpdate(SuccessMessageMixin, UpdateView):
	model = DemandTurnover
	template_name = "demand_turnover_edit.html"
	success_message = u"%(title)s 成功修改"
	fields = ["title", "note"]

	def get_success_url(self):
		self.url = reverse('approval:demand_turnover_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:demand_turnover_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(DemandTurnoverUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改管理人员需求与离职"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
