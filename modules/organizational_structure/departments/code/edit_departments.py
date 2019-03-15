# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.organizational_structure.departments.models import Department
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('departments.change_department', raise_exception=True))
class DepartmentEdit(UpdateView):
    model = Department
    template_name = "base/document_edit.html"
    fields = "__all__"

    def get_success_url(self):
        self.url = self.model.get_absolute_url()
        referrer = self.request.POST.get("referrer", "")
        if referrer:
            self.url = referrer
        _addanother = self.request.POST.get("_addanother", "")
        if _addanother:
            self.url = reverse('organizational_structure:departments:departments_add')
        return self.url

    def get_context_data(self, **kwargs):
        context = super(DepartmentEdit, self).get_context_data(**kwargs)
        context["form_content"] = u"修改部门信息"
        referrer = self.request.META.get('HTTP_REFERER', "")
        context["referrer"] = referrer
        return context
