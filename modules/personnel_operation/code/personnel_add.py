# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.organizational_structure.departments.models import Department
from modules.personnel_operation.models import QualityAssurance
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('personnel_operation.add_qualityassurance', raise_exception=True))
class PersonnelCreate(SuccessMessageMixin, CreateView):
	template_name = "personnel_edit.html"
	model = QualityAssurance
	success_message = u"%(problems_items)s 成功创建"
	fields = [
		"department",
		"project_id",
		"index_items",
		"problems_items",
		"problems_explain",
		"error_number",
		"provider",
		"error_date",
		"improve_time",
		"improve_status",
		"improve_date",
		"remark",
		"remark1",
		"remark2",
		"remark3"
	]

	def get_success_url(self):
		self.url = reverse('personnel_info:personnel_list', args=())
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('personnel_info:personnel_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(PersonnelCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"新增个人操作质量"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	# 将登陆用户作为申请人
	def form_valid(self, form):
		form.instance.create_user = self.request.user
		form.instance.department = Department.objects.filter(name=form.instance.department).first()
		return super(PersonnelCreate, self).form_valid(form)
