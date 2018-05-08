# coding=utf-8
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.approval_process.temporary_write_offs_billing.models import *
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(
	permission_required('temporary_write_offs_billing.add_temporarywriteoffsbilling', raise_exception=True))
class TemporaryWriteOffsBillingCreate(SuccessMessageMixin, CreateView):
	model = TemporaryWriteOffsBilling
	template_name = "temporary_write_offs_billing_edit.html"
	success_message = u"%(title)s 成功申请"
	fields = [
		"title",
		"note",
		"billing_month",
		"project_name",
		"billing_date_start",
		"billing_date_end",
		"billing_content",
		"billing_type",
		"management_fee",
		"wage_receive",
		"shuttle_fee_receive",
		"meals_receive",
		"dormitory_fee_receive",
		"daily_receive",
		"compensate_reparation_receive",
		"actual_outlay",
		"wage_outlay",
		"shuttle_fee_outlay",
		"meals_outlay",
		"daily_outlay",
		"compensate_reparation_outlay",
		"borrow_loan",
		"is_billing",
		"remark1",
	]

	def get_success_url(self):
		self.url = reverse('approval:temporary_write_offs_billing_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:temporary_write_offs_billing_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(TemporaryWriteOffsBillingCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"临时工销账与开票"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	# 将登陆用户作为申请人
	def form_valid(self, form):
		form.instance.apply_user = self.request.user
		form.instance.apply_types = "8"

		# 计算－主营业收入
		main_business_income = 0  # 主营业收入
		management_fee = self.request.POST.get("management_fee", 0)  # 管理费
		wage_receive = self.request.POST.get("wage_receive", 0)  # 工资(收)
		shuttle_fee_receive = self.request.POST.get("shuttle_fee_receive", 0)  # 班车费(收)
		meals_receive = self.request.POST.get("meals_receive", 0)  # 餐费(收)
		dormitory_fee_receive = self.request.POST.get("dormitory_fee_receive", 0)  # 宿舍费(收)
		daily_receive = self.request.POST.get("daily_receive", 0)  # 商报(收)
		compensate_reparation_receive = self.request.POST.get("compensate_reparation_receive", 0)  # 偿/赔偿金(收)
		if management_fee: main_business_income += int(management_fee)
		if wage_receive: main_business_income += int(wage_receive)
		if shuttle_fee_receive: main_business_income += int(shuttle_fee_receive)
		if meals_receive: main_business_income += int(meals_receive)
		if dormitory_fee_receive: main_business_income += int(dormitory_fee_receive)
		if daily_receive: main_business_income += int(daily_receive)
		if compensate_reparation_receive: main_business_income += int(compensate_reparation_receive)
		form.instance.main_business_income = main_business_income

		# 计算－主营业支出
		main_business_outlay = 0  # 主营业支出
		wage_outlay = self.request.POST.get("wage_outlay", 0)  # 工资(付)
		shuttle_fee_outlay = self.request.POST.get("shuttle_fee_outlay", 0)  # 班车费(付)
		meals_outlay = self.request.POST.get("meals_outlay", 0)  # 餐费(付)
		daily_outlay = self.request.POST.get("daily_outlay", 0)  # 商报(付)
		compensate_reparation_outlay = self.request.POST.get("compensate_reparation_outlay", 0)  # 赔偿/补偿金(付)
		borrow_loan = self.request.POST.get("borrow_loan", 0)  # 已借备用金

		if wage_outlay: main_business_outlay += int(wage_outlay)
		if shuttle_fee_outlay: main_business_outlay += int(shuttle_fee_outlay)
		if meals_outlay: main_business_outlay += int(meals_outlay)
		if daily_outlay: main_business_outlay += int(daily_outlay)
		if compensate_reparation_outlay: main_business_outlay += int(compensate_reparation_outlay)
		if borrow_loan: main_business_outlay += int(borrow_loan)
		form.instance.main_business_outlay = main_business_outlay

		# 计算-差额
		# 公式=已借备用金-主营业务支出，结果如果是正数，自动显示出：应返还公司XX钱；如果是负数，自动显示：公司应支付XX钱
		difference = 0
		try:
			difference = int(borrow_loan) - int(main_business_outlay)
		except:
			traceback.print_exc()
		form.instance.difference = difference

		return super(TemporaryWriteOffsBillingCreate, self).form_valid(form)


@class_view_decorator(login_required)
@class_view_decorator(
	permission_required('temporary_write_offs_billing.add_temporarywriteoffsbilling', raise_exception=True))
class TemporaryWriteOffsBillingDetailsCreate(SuccessMessageMixin, CreateView):
	model = TemporaryWriteOffsBillingDetails
	template_name = "temporary_write_offs_billing_details_edit.html"
	success_message = u"%(name)s 成功申请"
	fields = [
		"name", "sex", "identity_card_number", "project_name",
		"recruitment_attache", "phone_number", "start_work_date", "end_work_date", "work_days", "hours",
		"amount_of_payment", "release_user", "release_time", "remark1",
	]

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(TemporaryWriteOffsBillingDetailsCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"临时工销账与开票，明细申请"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def get_success_url(self):
		applicants = self.kwargs.get("applicants", 0)
		view_type = '1'
		self.url = reverse('approval:temporary_write_offs_billing_details_list', args=(applicants, view_type))

		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:temporary_write_offs_billing_details_add', args=(applicants))

		return self.url

	# 将登陆用户作为申请人
	def form_valid(self, form):
		try:
			applicants = self.kwargs.get("applicants", 0)
			form.instance.applicants = TemporaryWriteOffsBilling.objects.filter(
				id=applicants).first()  # 对应临时工销账与开票申请id

			# 校验当前登录用户，不是录入项目的负责人是，阻止录入
			login_user = self.request.user
			project_name = self.request.POST.get("project_name", 0)  # 项目名称
			if not project_name:
				messages.warning(self.request, u"请选择您所负责的“项目名称”")
				return super(TemporaryWriteOffsBillingDetailsCreate, self).form_invalid(form)

			project_name = Project.objects.filter(id=project_name)
			principal = ""
			if project_name.exists():
				principal = project_name[0].principal
			if login_user != principal:
				messages.warning(self.request, u"请选择您所负责的“项目名称”")
				return super(TemporaryWriteOffsBillingDetailsCreate, self).form_invalid(form)

			# 根据身份证号计算年龄
			now_year = datetime.datetime.now().year
			id_card = self.request.POST.get("identity_card_number", "")  # 身份证号
			age = self.request.POST.get("age", 0)
			if id_card and (age == "0" or not age):
				age_year_str = id_card[6:10]
				age = now_year - int(age_year_str)
			form.instance.age = int(age)

			# 计算性别
			sex = self.request.POST.get("sex", "")
			if id_card and not sex:
				sex_num = int(id_card[-2])
				if (sex_num % 2) == 0:
					sex = "F"
				else:
					sex = "M"
			form.instance.sex = sex
		except:
			traceback.print_exc()
		return super(TemporaryWriteOffsBillingDetailsCreate, self).form_valid(form)
