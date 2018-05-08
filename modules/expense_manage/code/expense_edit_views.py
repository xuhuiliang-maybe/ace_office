# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.expense_manage.models import Expense
from modules.share_module.check_decorator import check_principal
from modules.share_module.permissionMixin import class_view_decorator

"""
费用管理
"""


@class_view_decorator(login_required)
@class_view_decorator(permission_required('expense_manage.change_expense', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class ExpenseUpdate(SuccessMessageMixin, UpdateView):
	template_name = "expense_edit.html"
	model = Expense
	success_message = u"%(emplyid)s 成功修改"
	fields = "__all__"

	def get_success_url(self):
		self.url = reverse('expense_manage:expense_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('expense_manage:expense_add')

		return self.url

	def get_context_data(self, **kwargs):
		context = super(ExpenseUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改费用管理"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context
