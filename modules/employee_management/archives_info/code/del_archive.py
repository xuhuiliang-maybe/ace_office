# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import DeleteView

from modules.employee_management.employee_info.models import Archive
from modules.share_module.check_decorator import check_principal
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.delete_archive', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class ArchiveDelete(SuccessMessageMixin, DeleteView):
	model = Archive
	success_message = u"%(number)s 删除创建"
	template_name = "base/confirm_delete.html"

	def get_success_url(self):
		self.url = reverse('archive_info:archive_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		return self.url

	def get_context_data(self, **kwargs):
		context = super(ArchiveDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
