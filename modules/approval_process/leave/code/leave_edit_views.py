# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.approval_process.leave.models import Leave
from modules.share_module.check_decorator import check_is_approval
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('leave.change_leave', raise_exception=True))
@class_view_decorator(check_is_approval)
class LeaveUpdate(SuccessMessageMixin, UpdateView):
	model = Leave
	template_name = "leave_edit.html"
	success_message = u"%(title)s 成功修改"
	fields = ["title", "note", "begin_date", "end_date", "leave_type"]

	def get_success_url(self):
		self.url = reverse('approval:leave_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:leave_add')
		return self.url

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(LeaveUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改请假申请"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
