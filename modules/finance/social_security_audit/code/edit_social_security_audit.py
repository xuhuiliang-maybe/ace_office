# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView

from modules.finance.social_security_audit.models import *
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('social_security_audit.change_socialsecurityaudit', raise_exception=True))
# @class_view_decorator(check_principal)  # 校验是否负责该项目
class SocialSecurityAuditUpdate(SuccessMessageMixin, UpdateView):
	form_class = SocialSecurityAuditForm
	model = SocialSecurityAudit
	template_name = "social_security_audit_edit.html"
	success_message = u"%(remark)s 成功修改"

	def get_success_url(self):
		self.url = reverse('finance:social_security_audit:list_socialsecurityaudit', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('finance:social_security_audit:add_socialsecurityaudit')
		return self.url

	# 增加返回参数
	def get_context_data(self, **kwargs):
		context = super(SocialSecurityAuditUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改社保审核"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	# 表单处理
	def form_valid(self, form):
		identity_card_number = self.request.POST.get("identity_card_number", "")  # 身份证号
		name = ""  # 姓名
		social_security_billing = 0  # 社保结算
		social_security_outlay = 0  # 社保支出
		provident_fund_billing = 0  # 公积金结算
		provident_fund_outlay = 0  # 公积金支出

		# 查找姓名
		socialsecuritydetail = SocialSecurityDetail.objects.filter(identity_card_number=identity_card_number)
		payrolldetail = PayrollDetail.objects.filter(identity_card_number=identity_card_number)
		if socialsecuritydetail.exists():  # 社保明细
			name = socialsecuritydetail[0].name
			form.instance.name = name
		elif payrolldetail.exists():  # 薪资明细
			name = payrolldetail[0].name
			form.instance.name = name
		else:
			form.instance.name = name

		# 查找员工信息
		emp_obj = Employee.objects.filter(name=name, identity_card_number=identity_card_number)
		if emp_obj.exists():
			form.instance.employee = emp_obj[0]

		# --------------------------------------------------------------------------------
		# 社保结算
		if payrolldetail.exists():
			social_security_unit = payrolldetail[0].social_security_unit  # 社保单位
			person_social_security = payrolldetail[0].person_social_security  # 个人社保
			social_security_pay_unit = payrolldetail[0].social_security_pay_unit  # 社保补缴单位

			social_security_billing = social_security_unit + person_social_security + social_security_pay_unit
		form.instance.social_security_billing = social_security_billing

		# 社保支出
		if socialsecuritydetail.exists():
			social_security_person = socialsecuritydetail[0].social_security_person  # 社保个人
			social_security_company = socialsecuritydetail[0].social_security_company  # 社保公司
			social_security_pay_person = socialsecuritydetail[0].social_security_pay_person  # 社保补缴个人
			social_security_pay_company = socialsecuritydetail[0].social_security_pay_company  # 社保补缴公司
			social_security_outlay = social_security_person + social_security_company + social_security_pay_person + social_security_pay_company
		form.instance.social_security_outlay = social_security_outlay

		# 社保平衡
		social_security_balance = social_security_billing - social_security_outlay  # 社保平衡
		if social_security_balance == 0:
			form.instance.social_security_balance = '1'
		elif social_security_balance > 0:
			form.instance.social_security_balance = '2'
		elif social_security_balance < 0:
			form.instance.social_security_balance = '3'

		# --------------------------------------------------------------------------------
		# 公积金结算
		if payrolldetail.exists():
			provident_fund_unit = payrolldetail[0].provident_fund_unit  # 公积金单位
			person_provident_fund = payrolldetail[0].person_provident_fund  # 个人公积金
			provident_fund_pay_unit = payrolldetail[0].provident_fund_pay_unit  # 公积金补缴单位

			provident_fund_billing = provident_fund_unit + person_provident_fund + provident_fund_pay_unit
		form.instance.provident_fund_billing = provident_fund_billing

		# 公积金支出
		if socialsecuritydetail.exists():
			provident_fund_person = socialsecuritydetail[0].provident_fund_person  # 公积金个人
			provident_fund_company = socialsecuritydetail[0].provident_fund_company  # 公积金公司
			provident_fund_pay_person = socialsecuritydetail[0].provident_fund_pay_person  # 公积金补缴个人
			provident_fund_pay_company = socialsecuritydetail[0].provident_fund_pay_company  # 公积金补缴公司
			provident_fund_outlay = provident_fund_person + provident_fund_company + provident_fund_pay_person + provident_fund_pay_company
		form.instance.provident_fund_outlay = provident_fund_outlay

		# 公积金平衡
		provident_fund_balance = provident_fund_billing - provident_fund_outlay  # 公积金平衡
		if provident_fund_balance == 0:
			form.instance.provident_fund_balance = '1'
		elif provident_fund_balance > 0:
			form.instance.provident_fund_balance = '2'
		elif provident_fund_balance < 0:
			form.instance.provident_fund_balance = '3'

		return super(SocialSecurityAuditUpdate, self).form_valid(form)
