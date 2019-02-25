# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('auth.change_user', raise_exception=True))
class ProfileUpdate(SuccessMessageMixin, UpdateView):
	template_name = "profile_edit.html"
	model = User
	success_message = u"%(username)s 成功修改"

	# 保持与列表页相同顺序
	fields = (
		"company",
		# "one_level_dept",
		# "attribution_dept",
		"username",
		"first_name",
		"gender",
		"position",
		# "higher_up",
		# "email",
		"mobile_phone",
		"telephone",
		"address",
		"remark1",
		# "authorize_leave",
		# "authorize_loan",
		# "authorize_wage",
		"date_joined",
		"is_active",
		"dept_head",
		"is_superuser",
		"is_staff",
	)

	def get_success_url(self):
		self.url = reverse('organizational_structure:profile:profile_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('organizational_structure:profile:profile_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(ProfileUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改管理人员信息"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
