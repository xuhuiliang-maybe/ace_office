# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.share_module.check_decorator import check_principal
from modules.share_module.permissionMixin import class_view_decorator
from modules.social_security.social_security_detail.models import SocialSecurityDetail


@class_view_decorator(login_required)
@class_view_decorator(permission_required('social_security_detail.change_socialsecuritydetail', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class IncreaseUpdate(SuccessMessageMixin, UpdateView):
	"""编辑社保明细
	"""
	model = SocialSecurityDetail
	template_name = "social_security_detail_edit.html"
	success_message = u"%(computer_number)s 成功修改"
	fields = "__all__"

	def get_success_url(self):
		self.url = reverse('social_security_detail:reduction_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('social_security_detail:social_security_detail_add')
		return self.url

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(IncreaseUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改社保明细"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
