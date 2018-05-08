# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.approval_process.leave.models import Leave
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('leave.add_leave', raise_exception=True))
class LeaveCreate(SuccessMessageMixin, CreateView):
	model = Leave
	template_name = "leave_edit.html"
	success_message = u"%(title)s 成功申请"
	fields = ["title", "note", "begin_date", "end_date", "leave_type"]

	def get_success_url(self):
		self.url = reverse('approval:leave_list', args=())
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:leave_add')
		return self.url

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(LeaveCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"请假申请"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	# 将登陆用户作为申请人
	def form_valid(self, form):
		form.instance.apply_user = self.request.user
		form.instance.apply_types = "1"
		return super(LeaveCreate, self).form_valid(form)
