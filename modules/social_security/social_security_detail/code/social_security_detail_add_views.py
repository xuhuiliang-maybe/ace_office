# coding=utf-8
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.project_manage.models import Project
from modules.share_module.permissionMixin import class_view_decorator
from modules.social_security.social_security_detail.models import SocialSecurityDetail


# 新增，社保明细
@class_view_decorator(login_required)
@class_view_decorator(permission_required('social_security_detail.add_socialsecuritydetail', raise_exception=True))
class SocialSecurityDetailCreate(SuccessMessageMixin, CreateView):
	model = SocialSecurityDetail
	template_name = "social_security_detail_edit.html"
	success_message = u"%(computer_number)s 成功创建"
	fields = "__all__"

	def get_success_url(self):
		self.url = reverse('social_security_detail:reduction_list', args=())
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('social_security_detail:social_security_detail_add')
		return self.url

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(SocialSecurityDetailCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"新增社保明细"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def form_valid(self, form):
		# 校验当前登录用户，不是录入项目的负责人是，阻止录入
		try:
			login_user = self.request.user
			if not login_user.is_superuser:
				project_name = self.request.POST.get("project_name", 0)  # 项目名称
				if not project_name:
					messages.warning(self.request, u"请选择您所负责的“项目名称”")
					return super(SocialSecurityDetailCreate, self).form_invalid(form)

				project_obj = Project.objects.filter(id=project_name)
				principal = ""
				if project_obj.exists():
					principal = project_obj[0].principal
				if login_user != principal:
					messages.warning(self.request, u"请选择您所负责的“项目名称”")
					return super(SocialSecurityDetailCreate, self).form_invalid(form)
		except:
			traceback.print_exc()
		return super(SocialSecurityDetailCreate, self).form_valid(form)
