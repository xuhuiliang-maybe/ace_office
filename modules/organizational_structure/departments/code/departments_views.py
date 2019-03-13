# coding=utf-8
import json
import traceback

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.contrib.auth.models import User
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
        values = ["id", "name", "parent_dept", "apportion_type", "management_rights__name"]
        return Department.objects.filter(parent_dept=parent_id).values(*values)

    def update_dict(self, data_dict):
        dept_id = data_dict.get("id")
        apportion_type = data_dict.get("apportion_type")
        management_rights = data_dict.get("management_rights__name")
        if management_rights:
            management_rights = "(%s)" % management_rights
        else:
            management_rights = ""
        name_list = [
            data_dict.get("name"),
            "<small><sub>{} {}</sub></small>".format(management_rights,
                                                     Department.get_apportion_type(apportion_type))
        ]
        name = " ".join(name_list)
        return {
            "text": name,
            "type": "folder" if self.get_children(dept_id).exists() else "item",
            "value": dept_id
        }

    def level_dict(self, dept_id, id_dict, is_root=False, managements=[], edit_user_managements=[]):
        """
        :param dept_id: 部门ID
        :param id_dict:
        :param is_root:
        :param managements:登录用户授权的部门，过滤要显示的节点用
        :param edit_user_managements:正在编辑的用户已经授权的部门，节点默认选中用
        :return:
        """
        if is_root:
            return_value = {}
            children = self.get_children(dept_id)
            for child in children:
                dept_id = child.get('id')
                child = self.update_dict(child)
                return_value.update(
                    {str(dept_id): self.level_dict(dept_id, child, False, managements, edit_user_managements)})
            return return_value

        children = self.get_children(dept_id)
        if children or (dept_id in edit_user_managements):
            add_params = id_dict.setdefault('additionalParameters', {})
            if dept_id in edit_user_managements:
                add_params['item-selected'] = True
            if children:
                add_params['children'] = {}
                for child in children:
                    dept_id = child.get('id')
                    if not self.request.user.is_superuser:
                        if dept_id not in managements:
                            continue
                    child = self.update_dict(child)
                    add_params['children'][str(dept_id)] = self.level_dict(dept_id, child, False, managements,
                                                                           edit_user_managements)
        return id_dict

    def post(self, request, *args, **kwargs):
        try:
            # 用户授权管理部门
            managements = map(int, self.request.user.remark2.split(",")) if self.request.user.remark2 else []
            edit_user_id = self.request.POST.get("edit_user_id")
            edit_user_managements = list()
            if edit_user_id:
                try:
                    edit_user = User.objects.get(id=edit_user_id)
                    edit_user_managements = map(int, edit_user.remark2.split(",")) if edit_user.remark2 else []
                except:
                    pass

            # 优先在缓存获取部门树信息
            data = []  # cache.get("dept_tree_{}_{}".format(self.request.user.id,dept_models.DEPTVERSION))
            if not data:
                data = self.level_dict(0, None, True, managements, edit_user_managements)
                # cache.set("dept_tree_{}_{}".format(self.request.user.id,dept_models.DEPTVERSION), data)
            return HttpResponse(json.dumps(data))
        except:
            traceback.print_exc()
