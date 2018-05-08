# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.approval_process.loan.models import *
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('loan.add_loan', raise_exception=True))
class LoanCreate(SuccessMessageMixin, CreateView):
	template_name = "loan_edit.html"
	model = Loan
	success_message = u"%(title)s 成功申请"
	fields = ["title", "note", "money", "borrowing_date", "repayment_date"]

	def get_success_url(self):
		self.url = reverse('approval:loan_list', args=())
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:loan_add')
		return self.url

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(LoanCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"备用金申请"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	# 将登陆用户作为申请人
	def form_valid(self, form):
		form.instance.apply_user = self.request.user
		form.instance.apply_types = "2"  # 申请类型，参考模型
		return super(LoanCreate, self).form_valid(form)


@class_view_decorator(login_required)
@class_view_decorator(permission_required('loan.add_loan', raise_exception=True))
class LoanBudgetDetailsCreate(SuccessMessageMixin, CreateView):
	template_name = "base/document_edit.html"
	model = LoanBudgetDetails
	success_message = u"%(date_range)s 成功申请"
	fields = [
		# 临时工预算明细
		"date_range",
		"days",
		"daily_number",
		"hours_per_day",
		"hourly_wage",
		"meals_per_capita",
		"traffic_fee",

		# 其他预算明细
		"amount",
		"unit_price",
	]

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(LoanBudgetDetailsCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"备用金，费用预算明细申请"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def get_success_url(self):
		applicants = self.kwargs.get("applicants", 0)
		view_type = '1'
		self.url = reverse('approval:loan_budget_details_list', args=(applicants, view_type))

		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:loan_budget_details_add', args=(applicants))
		return self.url

	# 将登陆用户作为申请人
	def form_valid(self, form):
		try:
			applicants = self.kwargs.get("applicants", 0)
			form.instance.applicants = Loan.objects.filter(id=applicants).first()  # 对应备用金申请id

			# 计算临时工合计，天数*每天人数*每天人均工时*小时工资+人均餐费*每天人数+交通费
			days = int(self.request.POST.get("days", 0))  # 天数
			daily_number = int(self.request.POST.get("daily_number", 0))  # 每天人数
			hours_per_day = int(self.request.POST.get("hours_per_day", 0))  # 每天人均工时
			hourly_wage = int(self.request.POST.get("hourly_wage", 0))  # 小时工资
			meals_per_capita = int(self.request.POST.get("meals_per_capita", 0))  # 人均餐费
			traffic_fee = int(self.request.POST.get("traffic_fee", 0))  # 交通费
			# 临时工预算合计
			temporary_total = (days * daily_number * hours_per_day * hourly_wage) + (
				meals_per_capita * daily_number) + traffic_fee

			# 计算其他合计，数量*单价
			amount = int(self.request.POST.get("amount", 0))  # 数量
			unit_price = int(self.request.POST.get("unit_price", 0))  # 单价
			other_total = amount * unit_price

			# 计算总合计，其他预算合计+临时工预算合计
			form.instance.temporary_total = temporary_total  # 临时工预算合计
			form.instance.other_total = other_total  # 其他预算合计
			form.instance.all_total = temporary_total + other_total  # 总预算合计
		except:
			traceback.print_exc()
		return super(LoanBudgetDetailsCreate, self).form_valid(form)
