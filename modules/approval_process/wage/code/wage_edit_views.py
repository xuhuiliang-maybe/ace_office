# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.approval_process.wage.models import Wage
from modules.share_module.check_decorator import check_is_approval
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('wage.change_wage', raise_exception=True))
@class_view_decorator(check_is_approval)
class WageUpdate(SuccessMessageMixin, UpdateView):
	template_name = "base/document_edit.html"
	model = Wage
	success_message = u"%(title)s 成功修改"
	fields = ["title", "note", "money"]

	def get_success_url(self):
		self.url = reverse('approval:wage_list', args=())

		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:wage_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(WageUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改工资申请"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
