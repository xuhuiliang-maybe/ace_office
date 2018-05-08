# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.approval_process.billing_pre_pay.models import BillingPrePay
from modules.share_module.check_decorator import check_is_approval
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('billing_pre_pay.change_billingprepay', raise_exception=True))
@class_view_decorator(check_is_approval)
class BillingPrePayUpdate(SuccessMessageMixin, UpdateView):
	model = BillingPrePay
	template_name = "billing_pre_pay_edit.html"
	success_message = u"%(title)s 成功修改"
	fields = ["title", "note", "billingprepay_month", "project_name",
		  "billing_date_start",
		  "billing_date_end",
		  "billing_content",
		  "management_fee",
		  "wage_receive",
		  "social_security_receive",
		  "provident_fund_receive",
		  "union_fee_receive",
		  "disablement_gold",
		  "shuttle_fee_receive",
		  "meals_receive",
		  "dormitory_fee_receive",
		  "daily_receive",
		  "compensate_reparation_receive",
		  "bonus_receive",
		  "other_receive",
		  "ccb",
		  "merchants_bank",
		  "icbc",
		  "other_bank", "remark1"]

	def get_success_url(self):
		self.url = reverse('approval:billing_pre_pay_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:billing_pre_pay_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(BillingPrePayUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改结算与发薪"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def form_valid(self, form):
		# 计算－主营业收入
		main_business_income = 0  # 主营业收入
		management_fee = self.request.POST.get("management_fee", 0)  # 管理费
		wage_receive = self.request.POST.get("wage_receive", 0)  # 工资(收)
		social_security_receive = self.request.POST.get("social_security_receive", 0)  # 社保(收)
		provident_fund_receive = self.request.POST.get("provident_fund_receive", 0)  # 公积金(收)
		union_fee_receive = self.request.POST.get("union_fee_receive", 0)  # 工会费(收)
		disablement_gold = self.request.POST.get("disablement_gold", 0)  # 残保金
		shuttle_fee_receive = self.request.POST.get("shuttle_fee_receive", 0)  # 班车费(收)
		meals_receive = self.request.POST.get("meals_receive", 0)  # 餐费(收)
		dormitory_fee_receive = self.request.POST.get("dormitory_fee_receive", 0)  # 宿舍费(收)
		daily_receive = self.request.POST.get("daily_receive", 0)  # 商报(收)
		compensate_reparation_receive = self.request.POST.get("compensate_reparation_receive", 0)  # 偿/赔偿金(收)
		bonus_receive = self.request.POST.get("bonus_receive", 0)  # 奖金类(收)
		other_receive = self.request.POST.get("other_receive", 0)  # 其他收入
		if management_fee: main_business_income += int(management_fee)
		if wage_receive: main_business_income += int(wage_receive)
		if social_security_receive: main_business_income += int(social_security_receive)
		if provident_fund_receive: main_business_income += int(provident_fund_receive)
		if union_fee_receive: main_business_income += int(union_fee_receive)
		if disablement_gold: main_business_income += int(disablement_gold)
		if shuttle_fee_receive: main_business_income += int(shuttle_fee_receive)
		if meals_receive: main_business_income += int(meals_receive)
		if dormitory_fee_receive: main_business_income += int(dormitory_fee_receive)
		if daily_receive: main_business_income += int(daily_receive)
		if compensate_reparation_receive: main_business_income += int(compensate_reparation_receive)
		if bonus_receive: main_business_income += int(bonus_receive)
		if other_receive: main_business_income += int(other_receive)

		form.instance.main_business_income = main_business_income

		# 计算－发放总额
		grant_total = 0  # 发放总额
		ccb = self.request.POST.get("ccb", 0)  # 建行
		merchants_bank = self.request.POST.get("merchants_bank", 0)  # 招行
		icbc = self.request.POST.get("icbc", 0)  # 工行
		other_bank = self.request.POST.get("other_bank", 0)  # 其他银行

		if ccb: grant_total += int(ccb)
		if merchants_bank: grant_total += int(merchants_bank)
		if icbc: grant_total += int(icbc)
		if other_bank: grant_total += int(other_bank)
		form.instance.grant_total = grant_total

		return super(BillingPrePayUpdate, self).form_valid(form)
