# coding=utf-8
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.payroll_manage.payroll_detail.models import PayrollDetail
from modules.project_manage.models import Project
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('payroll_manage.add_payrolldetail', raise_exception=True))
class PayrollDetailCreate(SuccessMessageMixin, CreateView):
	model = PayrollDetail
	template_name = "payroll_detail_edit.html"
	fields = "__all__"
	success_message = u"%(name)s 成功创建"

	def get_success_url(self):
		self.url = reverse('payroll_manage:payroll_detail:payroll_detail_list', args=())
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('payroll_manage:payroll_detail:payroll_detail_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(PayrollDetailCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"新增薪资明细"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def form_valid(self, form):
		# 校验当前登录用户，不是录入项目的负责人是，阻止录入
		try:
			login_user = self.request.user
			project_name = self.request.POST.get("project_name", 0)  # 项目名称
			if not project_name:
				messages.warning(self.request, u"请选择您所负责的“项目名称”")
				return super(PayrollDetailCreate, self).form_invalid(form)

			project_obj = Project.objects.filter(id=project_name)
			principal = ""
			if project_obj.exists():
				principal = project_obj[0].principal
			if login_user != principal:
				messages.warning(self.request, u"请选择您所负责的“项目名称”")
				return super(PayrollDetailCreate, self).form_invalid(form)
		except:
			traceback.print_exc()
		return super(PayrollDetailCreate, self).form_valid(form)
