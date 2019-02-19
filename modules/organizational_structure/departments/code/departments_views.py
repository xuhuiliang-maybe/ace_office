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

	def post(self, request, *args, **kwargs):
		try:
			# 优先在缓存获取部门树信息
			# dept_tree = cache.get("dept_tree_%s" % dept_models.DEPTVERSION)
			# if dept_tree:
			# 	return HttpResponse(dept_tree)

			all_dept_obj = Department.get_all_dept()

			self.result_dict = dict()  # 最终返回部门树字典
			self.not_find_parent = list()  # 暂时未找到上级部门的部门信息
			if not all_dept_obj:  # 没有部门信息
				default_dict = {"0": {'text': '无', 'type': 'item'}}
				self.result_dict.update(default_dict)
			else:
				for dept_obj in all_dept_obj:
					dept_id = dept_obj.id  # 部门id
					dept_name = dept_obj.name  # 部门名称
					parent_id = dept_obj.parent_dept  # 父部门id
					apportion_type = dept_obj.apportion_type  # 分摊类型

					# 当前部门信息，父部门id是0，代表没有上级部门，为根部门
					if parent_id == 0:
						# 创建根部门结构
						root_dep_dict = dict()
						detail_dict = dict()

						detail_dict['text'] = Department.get_apportion_type(
							apportion_type) + dept_name
						detail_dict['value'] = dept_id
						detail_dict['type'] = 'item'
						has_child = dept_obj.getChildren()
						if has_child.exists():
							detail_dict['type'] = 'folder'
							detail_dict["additionalParameters"] = dict()
							detail_dict["additionalParameters"]['children'] = dict()
						# detail_dict["additionalParameters"]['item-selected'] = True  # 默认展开跟部门

						root_dep_dict[dept_id] = detail_dict
						self.result_dict.update(root_dep_dict)  # 添加到最终返回树形列表
						continue

					# 当前部门信息，父部门id不为0，存在上级部门
					if parent_id != 0:
						# 为父节点添加子节点
						new_result_dict = self.update_result_dict(self.result_dict, dept_obj)

						# 当前节点不能作为子节点添加到父节点，创建当前节点为根节点
						if not new_result_dict:  # 没有根节点
							root_dep_dict = dict()
							detail_dict = dict()

							detail_dict['text'] = Department.get_apportion_type(
								apportion_type) + dept_name
							detail_dict['value'] = dept_id
							detail_dict['type'] = 'item'
							has_child = dept_obj.getChildren()
							if has_child.exists():
								detail_dict['type'] = 'folder'
								detail_dict["additionalParameters"] = dict()
								detail_dict["additionalParameters"]['children'] = dict()

							root_dep_dict[dept_id] = detail_dict
							self.result_dict.update(root_dep_dict)  # 添加到最终返回树形列表

			self.not_find_parent = list(set(self.not_find_parent))
			if self.not_find_parent:
				for dept_obj in self.not_find_parent:
					self.update_result_dict(self.result_dict, dept_obj)

			result = json.dumps(self.result_dict)
			# cache.set("dept_tree_%s" % dept_models.DEPTVERSION, result)
			return HttpResponse(result)
		except:
			traceback.print_exc()

	def update_result_dict(self, result_dict, dept_obj):
		try:
			# 存在部门信息，没有返回空列表
			if result_dict:
				for index in result_dict:
					dept_id = dept_obj.id
					dept_name = dept_obj.name
					parent_id = dept_obj.parent_dept
					apportion_type = dept_obj.apportion_type  # 分摊类型

					# 判断当前节点是否是新增节点的父节点
					if result_dict.has_key(parent_id):
						new_sub_dict = dict()
						new_sub_detail_dict = dict()

						new_sub_detail_dict['text'] = Department.get_apportion_type(
							apportion_type) + dept_name
						new_sub_detail_dict['value'] = dept_id
						new_sub_detail_dict['type'] = 'item'
						has_child = dept_obj.getChildren()
						if has_child.exists():
							new_sub_detail_dict['type'] = 'folder'
							new_sub_detail_dict["additionalParameters"] = dict()
							new_sub_detail_dict["additionalParameters"]['children'] = dict()

						new_sub_dict[dept_id] = new_sub_detail_dict
						result_dict[parent_id]["additionalParameters"]['children'].update(
							new_sub_dict)
						return True
					elif result_dict[index].get("additionalParameters", {}).get('children'):
						# 递归调用，查询树形节点域当前节点的关系
						if self.update_result_dict(result_dict[index]["additionalParameters"]['children'], dept_obj):
							return True
					elif parent_id != 0:
						self.not_find_parent.append(dept_obj)
						return True
			return False
		except:
			traceback.print_exc()
