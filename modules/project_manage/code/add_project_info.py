# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView

from modules.project_manage.models import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs


@class_view_decorator(login_required)
@class_view_decorator(permission_required('project_manage.add_project', raise_exception=True))
class ProjectsCreate(SuccessMessageMixin, CreateView):
	model = Project
	template_name = "projects_edit.html"
	form_class = ProjectForm
	success_message = u"%(full_name)s 成功创建"

	def get_success_url(self):
		self.url = reverse('project_manage:project_list', args=("basic_info",))
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('project_manage:project-add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(ProjectsCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"新增项目基础信息"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def form_valid(self, form):
		try:
			principal = ""
			customer_service_staff = self.request.POST.get("customer_service_staff", "")  # 客服专员
			customer_service_charge = self.request.POST.get("customer_service_charge", "")  # 客服主管
			outsource_director = self.request.POST.get("outsource_director", "")  # 外包主管
			customer_service_director = self.request.POST.get("customer_service_director", "")  # 客服经理
			other_responsible_person = self.request.POST.get("other_responsible_person", "")  # 其他负责人
			if customer_service_staff:
				principal = customer_service_staff
			elif customer_service_charge:
				principal = customer_service_charge
			elif outsource_director:
				principal = outsource_director
			elif customer_service_director:
				principal = customer_service_director
			elif other_responsible_person:
				principal = other_responsible_person

			search_condition = {"id": principal}
			kwargs = get_kwargs(search_condition)
			if kwargs:
				temp_user = User.objects.filter(**kwargs)
				if temp_user.exists():
					form.instance.principal = temp_user.first()
			return super(ProjectsCreate, self).form_valid(form)
		except:
			traceback.print_exc()
