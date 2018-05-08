# coding=utf-8
import json
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import DeleteView

from modules.share_module.check_decorator import check_principal
from modules.share_module.permissionMixin import class_view_decorator
from modules.social_security.social_security_detail.models import SocialSecurityDetail


@class_view_decorator(login_required)
@class_view_decorator(permission_required('social_security_detail.delete_socialsecuritydetail', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class SocialSecurityDetailDelete(SuccessMessageMixin, DeleteView):
	model = SocialSecurityDetail
	template_name = "base/confirm_delete.html"
	success_message = u"%(computer_number)s 删除创建"

	def get_success_url(self):
		self.url = reverse('social_security_detail:reduction_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(SocialSecurityDetailDelete, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context


@class_view_decorator(login_required)
@class_view_decorator(permission_required('social_security_detail.delete_socialsecuritydetail', raise_exception=True))
class SocialSecurityDetailBatchDelete(SuccessMessageMixin, View):
	def post(self, request, *args, **kwargs):
		try:
			ids = request.POST.get('ids').split(",")
			detail_obj_list = SocialSecurityDetail.objects.filter(id__in=ids)
			for one_obj in detail_obj_list:
				try:
					if one_obj.project_name.principal == request.user or request.user.is_superuser:
						one_obj.delete()
				except:
					traceback.print_exc()
			messages.success(self.request, u"成功删除")
			result = {"code": 1, "msg": "成功删除"}
		except:
			traceback.print_exc()
			messages.warning(self.request, u"删除操作异常")
			result = {"code": -1, "msg": "删除异常"}

		return HttpResponse(json.dumps(result), content_type="application/json")
