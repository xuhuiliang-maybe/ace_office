# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models

from modules.project_manage.models import Project


class PayrollDetail(models.Model):
	"""薪资明细 """
	name = models.CharField(u"姓名", max_length=256)
	identity_card_number = models.CharField(u"身份证号", max_length=18)
	project_name = models.ForeignKey(Project, verbose_name=u"项目名称", related_name="payroll_detal_project")
	settle_accounts_month = models.DateField(u"结算月份")
	wages_should_be = models.PositiveIntegerField(u"应发工资", null=True, blank=True)
	person_social_security = models.PositiveIntegerField(u"个人社保", null=True, blank=True)
	person_provident_fund = models.PositiveIntegerField(u"个人公积金", null=True, blank=True)
	pre_tax_adjustment = models.PositiveIntegerField(u"税前调整", null=True, blank=True)
	pre_tax_wage = models.PositiveIntegerField(u"税前工资", null=True, blank=True)
	tax = models.PositiveIntegerField(u"个税", null=True, blank=True)
	tax_rate = models.PositiveIntegerField(u"税率", null=True, blank=True)
	quick_deduction = models.PositiveIntegerField(u"速算扣除数", null=True, blank=True)
	tax_adjustments = models.PositiveIntegerField(u"税后调整", null=True, blank=True)
	real_hair_wage = models.PositiveIntegerField(u"实发工资", null=True, blank=True)
	social_security_unit = models.PositiveIntegerField(u"社保单位", null=True, blank=True)
	provident_fund_unit = models.PositiveIntegerField(u"公积金单位", null=True, blank=True)
	social_security_pay_unit = models.PositiveIntegerField(u"社保补缴单位", null=True, blank=True)
	provident_fund_pay_unit = models.PositiveIntegerField(u"公积金补缴单位", null=True, blank=True)
	social_security_provident_fund_sum_unit = models.PositiveIntegerField(u"社保+公积金合计单位", null=True, blank=True)
	employer = models.PositiveIntegerField(u"雇主/商保/意外险", null=True, blank=True)
	security_for_disabled = models.PositiveIntegerField(u"残疾人保障金", null=True, blank=True)
	management_fee = models.PositiveIntegerField(u"管理费", null=True, blank=True)
	total = models.PositiveIntegerField(u"合计", null=True, blank=True)
	remark = models.CharField(u"备注", max_length=256, null=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"薪资明细"
		ordering = ['-id']  # id倒叙
		index_together = ["project_name", "settle_accounts_month"]  # 索引字段组合
		permissions = (
			("browse_payrolldetail", u"浏览 薪资明细"),
		)

	def get_absolute_url(self):
		return reverse('payroll_manage:payroll_detail:payroll_detail_list')
