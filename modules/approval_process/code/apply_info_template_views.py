# coding=utf-8
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic.base import TemplateView

from modules.share_module.permissionMixin import class_view_decorator


# 申请信息模板默认页面
@class_view_decorator(login_required)
@class_view_decorator(permission_required('admin_account.browse_apply_info_template', raise_exception=True))
class ApplyTemplateInfoView(TemplateView):
	template_name = "all_apply_list.html"

	def get_context_data(self, **kwargs):
		context = super(ApplyTemplateInfoView, self).get_context_data(**kwargs)
		context["title"] = ""
		context["status"] = ""
		context["apply_type"] = "none"  # 申请类型，说明页面
		
		# 查看方式，# 1:由明细表返回，申请页面带查询条件，2：由待审批超链进去，不带查询条件
		context["view_type"] = "1"
		return context
