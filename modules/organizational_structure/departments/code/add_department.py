# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.organizational_structure.departments.models import Department
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('departments.add_department', raise_exception=True))
class DepartmentsAdd(CreateView):
	model = Department
	template_name = "base/document_edit.html"
	fields = "__all__"

	def get_success_url(self):
		self.url = reverse('organizational_structure:departments:departments_list', args=())
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('organizational_structure:departments:departments_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(DepartmentsAdd, self).get_context_data(**kwargs)
		context["form_content"] = u"新增部门信息"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context