# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.views.generic import ListView

from modules.organizational_structure.departments.models import Department
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE


@class_view_decorator(login_required)
@class_view_decorator(permission_required('admin_account.browse_user', raise_exception=True))
class ProfileList(ListView):
    context_object_name = "profile_list"
    template_name = "profile_list.html"
    allow_empty = True
    paginate_by = PAGINATE

    def get_queryset(self):
        self.dept_ids = self.request.GET.get("dept_ids", "")
        self.dept_name = self.request.GET.get("dept_name", "")
        self.first_name = self.request.GET.get("first_name", "")

        search_condition = {
            "first_name__icontains": self.first_name,
        }
        if self.dept_name:
            search_condition.update({"attribution_dept__in": self.dept_name.split(",")})
        else:
            if not self.request.user.is_superuser:
                managements = map(int, self.request.user.remark2.split(",")) if self.request.user.remark2 else []
                department_name_list = Department.objects.filter(id__in=managements).values_list("name", flat=True)
                search_condition.update({"attribution_dept__in": department_name_list})

        kwargs = get_kwargs(search_condition)
        return User.objects.filter(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileList, self).get_context_data(**kwargs)
        context["dept_name"] = self.dept_name
        context["dept_ids"] = self.dept_ids
        context["first_name"] = self.first_name
        return context
