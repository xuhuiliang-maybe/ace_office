# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import DeleteView

from modules.personnel_operation.models import QualityAssurance
from modules.share_module.check_decorator import check_principal
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('personnel_operation.delete_qualityassurance', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class PersonnelDelete(SuccessMessageMixin, DeleteView):
	model = QualityAssurance
	template_name = "base/confirm_delete.html"
	success_message = u"%(problems_items)s 删除创建"

	def get_success_url(self):
		self.url = reverse('personnel_info:personnel_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(PersonnelDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
