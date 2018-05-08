# coding=utf-8
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.views.generic import View

from modules.approval_process.models import PendingApproval
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('approval_process.change_pendingapproval', raise_exception=True))
class PendingActionView(View):
	""" 待审批操作处理 """

	def post(self, request, *args, **kwargs):
		try:
			oper = self.request.POST.get("oper", "")  # refuse:拒绝   agree：同意
			pending_id = self.request.POST.get("pending_id", "")  # 待审批数据id
			reson = self.request.POST.get("reson", "")  # 审批回复，拒绝才会有
			handle_user = self.request.user

			if pending_id and oper:
				event_obj = PendingApproval.objects.get(id=pending_id)
				permission_result = event_obj.event.check_permission(handle_user)  # 判断是否有权限审核
				if not permission_result:
					return HttpResponse(u"您的审批权限不足！")

				if oper == "agree":  # 通过
					result = event_obj.event.agree_apply(handle_user)
					return HttpResponse(result)
				elif oper == "refuse":  # 拒绝
					event_obj.event.refuse_apply(handle_user, reson)
					return HttpResponse(u"操作成功")

			return HttpResponse(u"操作失败！")
		except:
			traceback.print_exc()
			return HttpResponse(u"操作异常！")
