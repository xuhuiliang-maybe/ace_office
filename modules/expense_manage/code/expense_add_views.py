# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.expense_manage.models import Expense
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('expense_manage.add_expense', raise_exception=True))
class ExpenseCreate(SuccessMessageMixin, CreateView):
	model = Expense
	template_name = "expense_edit.html"
	fields = "__all__"
	success_message = u"%(emplyid)s 成功创建"

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
		context = super(ExpenseCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"新增费用管理"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def form_valid(self, form):
		return super(ExpenseCreate, self).form_valid(form)
