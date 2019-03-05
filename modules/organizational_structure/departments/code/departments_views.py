# coding=utf-8
import json
import traceback

from django.contrib.auth.decorators import login_required
# from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View

from modules.organizational_structure.departments import models as dept_models
from modules.organizational_structure.departments.models import Department
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
# @class_view_decorator(permission_required('admin_account.browse_department', raise_exception=True))
class DepartmentsListView(View):
    def get(self, request, *args, **kwargs):
        try:
            template_name = "departments_info.html"
            return render_to_response(template_name, {}, context_instance=RequestContext(request))
        except:
            traceback.print_exc()

    def get_children(self, parent_id):
        return Department.objects.filter(parent_dept=parent_id).values("id", "name", "parent_dept", "apportion_type")

    def update_dict(self, data_dict):
        dept_id = data_dict.get("id")
        apportion_type = data_dict.get("apportion_type")
        name = Department.get_apportion_type(apportion_type) + data_dict.get("name")
        return {
            "text": name,
            "type": "folder" if self.get_children(dept_id).exists() else "item",
            "value": dept_id
        }

    def level_dict(self, id, id_dict, is_root=False):
        if is_root:
            return_value = {}
            children = self.get_children(id)
            for child in children:
                id = child.get('id')
                child = self.update_dict(child)
                return_value.update({str(id): self.level_dict(id, child)})
            return return_value
        children = self.get_children(id)
        if children:
            add_params = id_dict.setdefault('additionalParameters', {})
            add_params['children'] = {}
            for child in children:
                id = child.get('id')
                child = self.update_dict(child)
                add_params['children'][str(id)] = self.level_dict(id, child)
        return id_dict

    def post(self, request, *args, **kwargs):
        try:
            # 优先在缓存获取部门树信息
            # dept_tree = cache.get("dept_tree_%s" % dept_models.DEPTVERSION)
            # if dept_tree:
            # 	return HttpResponse(dept_tree)
            data = self.level_dict(0, None, True)
            return HttpResponse(json.dumps(data))
        # cache.set("dept_tree_%s" % dept_models.DEPTVERSION, result)
        except:
            traceback.print_exc()
