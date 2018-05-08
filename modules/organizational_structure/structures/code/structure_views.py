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

	def post(self, request, *args, **kwargs):
		try:
			action = self.request.POST.get("action", "")
			# [{"id": "1", "pid": "0", "name": "aaa", "childrens": []}]，最终返回数据结构
			self.not_find_parent = list()  # 暂时未找到上级部门的部门信息
			self.result_list = dict()  # 最终返回树形列表

			if action == "org_select":  # 取架构数据
				all_dept_list = Department.get_all_dept()
				if not all_dept_list:
					default_dict = {"0": {"name": "无", "pid": "", "childrens": dict()}}
					self.result_list.update(default_dict)
				else:
					for one_dept_dict in all_dept_list:
						dept_id = one_dept_dict.id  # 部门id
						dept_name = one_dept_dict.name  # 部门名称
						parent_id = one_dept_dict.parent_dept  # 父部门id
						apportion_type = one_dept_dict.apportion_type  # 分摊类型

						# 当前部门信息，父部门id是0，代表没有上级部门，为根跟部门
						if parent_id == 0:
							# 创建根部门结构
							root_dep_dict = {
								dept_id: {
									"name": Department.get_apportion_type(
										apportion_type) + dept_name,
									"pid": parent_id,
									"childrens": dict()
								}
							}
							self.result_list.update(root_dep_dict)  # 添加到最终返回树形列表
							continue

						# 当前部门信息，父部门id不为0，存在上级部门
						if parent_id != 0:
							# 为父节点添加子节点
							new_result_list = self.update_result_list(self.result_list,
												  one_dept_dict)

							# 当前节点不能作为子节点添加到父节点，创建当前节点为根节点
							if not new_result_list:  # 没有根节点
								root_dep_dict = {
									dept_id: {
										"name": Department.get_apportion_type(
											apportion_type) + dept_name,
										"pid": parent_id,
										"childrens": dict()
									}
								}
								self.result_list.update(root_dep_dict)  # 添加到最终返回树形列表

			if self.not_find_parent:
				for one_dept_dict in self.not_find_parent:
					self.update_result_list(self.result_list, one_dept_dict)

			results = json.dumps(self.result_list)
			return HttpResponse(results)
		except:
			traceback.print_exc()

	def update_result_list(self, result_list, one_dept_dict):
		try:
			# 存在跟部门信息，没有返回空列表
			if result_list:
				for index in result_list:
					dept_id = one_dept_dict.id
					dept_name = one_dept_dict.name
					parent_id = one_dept_dict.parent_dept
					apportion_type = one_dept_dict.apportion_type  # 分摊类型

					# 查询当前节点的id是否与新的树形数组的id一致，如果是，那么将当前节点存放在树形数组的childrens字段中
					if result_list.has_key(parent_id):
						one_dict_root = {}
						one_dict = dict()
						one_dict["name"] = Department.get_apportion_type(apportion_type)+dept_name
						one_dict["pid"] = parent_id
						one_dict["childrens"] = dict()
						one_dict_root[dept_id] = one_dict
						result_list[parent_id]["childrens"].update(one_dict_root)
						return True
					elif result_list[index]["childrens"]:  # 父节点有子节点
						# 递归调用，查询树形节点域当前节点的关系
						if self.update_result_list(result_list[index]["childrens"], one_dept_dict):
							return True
					elif parent_id != 0:
						if one_dept_dict not in self.not_find_parent:
							self.not_find_parent.append(one_dept_dict)
						return True
			return False
		except:
			traceback.print_exc()
