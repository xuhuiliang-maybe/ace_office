# coding=utf-8
import json
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View

from modules.organizational_structure.departments.models import Department
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('admin_account.browse_structure', raise_exception=True))
class StructureListView(View):
    def get(self, request, *args, **kwargs):
        try:
            template_name = "structure_info.html"
            return render_to_response(template_name, {}, context_instance=RequestContext(request))
        except:
            traceback.print_exc()

    def get_children(self, parent_id):
        return Department.objects.filter(parent_dept=parent_id).values("id", "name", "parent_dept", "apportion_type")

    def update_dict(self, data_dict):
        parent_dept = data_dict.get("parent_dept")
        apportion_type = data_dict.get("apportion_type")
        name = Department.get_apportion_type(apportion_type) + data_dict.get("name")
        return {
            "name": name,
            "pid": parent_dept
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
            add_params = id_dict.setdefault('childrens', {})
            for child in children:
                id = child.get('id')
                child = self.update_dict(child)
                add_params[str(id)] = self.level_dict(id, child)
        return id_dict

    def post(self, request, *args, **kwargs):
        try:
            data = self.level_dict(0, None, True)
            return HttpResponse(json.dumps(data))
        except:
            traceback.print_exc()
