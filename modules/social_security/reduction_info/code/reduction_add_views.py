# coding=utf-8
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.employee_management.employee_info.models import Employee
from modules.share_module.permissionMixin import class_view_decorator
from modules.social_security.reduction_info.models import Reduction


@class_view_decorator(login_required)
@class_view_decorator(permission_required('reduction_info.add_reduction', raise_exception=True))
class ReductionCreate(SuccessMessageMixin, CreateView):
	model = Reduction
	template_name = "base/document_edit.html"
	fields = ["emplyid", "remark", "remark1", "remark2"]
	success_message = u"%(emplyid)s 成功创建"

	def get_success_url(self):
		self.url = reverse('reduction_info:reduction_list', args=())
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('reduction_info:reduction_add')
		return self.url

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(ReductionCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"新增减员信息"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def form_valid(self, form):
		# 校验当前登录用户，不是录入项目的负责人是，阻止录入
		try:
			login_user = self.request.user
			emplyid = self.request.POST.get("emplyid", 0)  # 员工编号
			if not emplyid:
				messages.warning(self.request, u"请选择您所负责的“员工编号”")
				return super(ReductionCreate, self).form_invalid(form)

			emp_obj = Employee.objects.filter(id=emplyid)
			principal = ""
			if emp_obj.exists():
				principal = emp_obj[0].project_name.principal
			if login_user != principal:
				messages.warning(self.request, u"请选择您所负责的“员工编号”")
				return super(ReductionCreate, self).form_invalid(form)
		except:
			traceback.print_exc()
		return super(ReductionCreate, self).form_valid(form)
