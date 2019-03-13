# coding=utf-8
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.views.generic import View

from modules.organizational_structure.departments.models import Department
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('departments.delete_department', raise_exception=True))
class DepartmentsDelView(View):
	def post(self, request, *args, **kwargs):
		message_dict = {
			"1": u"成功删除部门!",
			"2": u"要删除的部门不存在!",
			"3": u"总部门不能删除!",
			"4": u"删除部门有下级部门不能删除！",
			"5": u"删除部门失败！",
		}

		try:
			# 获取参数
			dept_id = self.request.POST.get("dept_id", "")  # 部门名称

			# 获取部门
			dept = Department.get_dept_by_id(dept_id)
			if dept:
				if dept.parent_dept == 0:
					return HttpResponse(message_dict["3"])
				else:
					if dept.get_children():
						return HttpResponse(message_dict["4"])
					else:
						dept.delete()
						return HttpResponse(message_dict["1"])
			else:
				return HttpResponse(message_dict["2"])

		except:
			traceback.print_exc()
			return HttpResponse(message_dict["5"])
