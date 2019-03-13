# coding=utf-8
import json
import sys

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import DeleteView

from modules.project_manage.models import *
from modules.share_module.check_decorator import check_principal
from modules.share_module.permissionMixin import class_view_decorator

reload(sys)
sys.setdefaultencoding('utf-8')


@class_view_decorator(login_required)
@class_view_decorator(permission_required('project_manage.delete_project', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class ProjectsDelete(SuccessMessageMixin, DeleteView):
	model = Project
	template_name = "base/confirm_delete.html"
	success_message = u"%(short_name)s 删除创建"

	def get_success_url(self):
		self.url = reverse('project_manage:project_list', args=("basic_info",))
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		kwargs["referrer"] = self.request.META.get('HTTP_REFERER', "")
		kwargs["help_text"] = u"项目关联员工信息会一并删除！"
		return super(ProjectsDelete, self).get_context_data(**kwargs)


@class_view_decorator(login_required)
@class_view_decorator(permission_required('project_manage.delete_project', raise_exception=True))
class ProjectsBatchDelete(SuccessMessageMixin, View):
	def post(self, request, *args, **kwargs):
		result = {"code": 1, "msg": "成功删除"}
		try:
			ids = request.POST.get('ids').split(",")
			project_obj = Project.objects.filter()
			if ids[0] == "all":
				if request.user.is_superuser:
					project_obj.all().delete()
					messages.success(self.request, u"成功删除")
					result = {"code": -1, "msg": u"成功删除"}
					return HttpResponse(json.dumps(result), content_type="application/json")
				else:
					project_obj_list = project_obj.all()
			else:
				project_obj_list = project_obj.filter(id__in=ids)

			for one_obj in project_obj_list:
				try:
					if one_obj.principal == request.user:
						one_obj.delete()
				except:
					traceback.print_exc()
			messages.success(self.request, u"成功删除")
		except:
			traceback.print_exc()
			messages.warning(self.request, u"删除操作异常")
			result = {"code": -1, "msg": u"删除异常"}
		finally:
			return HttpResponse(json.dumps(result), content_type="application/json")
