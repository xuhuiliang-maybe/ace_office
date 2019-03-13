# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from modules.project_manage.models import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE

"""
项目基础信息
"""


@class_view_decorator(login_required)
class ProjectsList(ListView):
    context_object_name = "projects_list"
    template_name = "projects_list.html"
    allow_empty = True
    paginate_by = PAGINATE

    def get_queryset(self):
        # 查询条件
        self.search_name = self.request.GET.get("search_name", "")
        self.dept_ids = self.request.GET.get("dept_ids", "")
        self.dept_name = self.request.GET.get("dept_name", "")
        try:
            self.progress_state = int(self.request.GET.get("progress_state", 1))  # 目前状态
        except:
            self.progress_state = 0

        # 判断是否是客服部,是，只显示当前用户所属部门下信息
        self.customer_service = 0
        # try:
        #     user_position = self.request.user.position.name  # 用户岗位
        # except:
        #     user_position = ""
        # position_list = [u"客服专员", u"客服主管", u"外包主管", u"客服经理"]
        # if user_position in position_list:  # 登录用户在客服部，只能查看所在部门项目信息
        #     self.dept_name = self.request.user.attribution_dept
        #     self.customer_service = 1

        search_condition = {
            "full_name__icontains": self.search_name,
            "progress_state": self.progress_state
        }
        if self.dept_name:
            search_condition.update({"department__name__in": self.dept_name.split(",")})
        else:
            if not self.request.user.is_superuser and not self.request.user.dept_head:
                managements = map(int, self.request.user.remark2.split(",")) if self.request.user.remark2 else []
                search_condition.update({"department__id__in": managements})

        kwargs = get_kwargs(search_condition)
        return Project.objects.filter(**kwargs)

    def get_context_data(self, **kwargs):
        project_info_type = self.kwargs.get("project_info_type", "")  # 项目信息类型
        perm = self.request.user.has_perm('project_manage.browse_%s' % project_info_type)
        if not perm:
            raise PermissionDenied

        kwargs["dept_name"] = self.dept_name
        kwargs["dept_ids"] = self.dept_ids
        kwargs["search_name"] = self.search_name
        kwargs["customer_service"] = self.customer_service
        kwargs["project_info_type"] = project_info_type
        kwargs["progress_state_list"] = ProgressState.objects.all()
        kwargs["progress_state"] = self.progress_state
        return super(ProjectsList, self).get_context_data(**kwargs)
