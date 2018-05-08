# coding=utf-8
from django.db import models

from modules.project_manage.models import Project

SERVICE_COMPANY = (
	('1', u'邦泰'),
	('2', u'杰博'),
)


class SocialSecurityDetail(models.Model):
	""" 社保明细 """
	computer_number = models.CharField(u"社保电脑号", max_length=200, blank=True)
	service_company = models.CharField(u"服务公司", max_length=1, choices=SERVICE_COMPANY)
	proxy_company = models.CharField(u"代理公司", max_length=200, blank=True)
	name = models.CharField(u"姓名", max_length=200)
	project_name = models.ForeignKey(Project, verbose_name=u"项目名称")
	account_nature = models.CharField(u"户口性质", max_length=200, blank=True)
	identity_card_number = models.CharField(u"身份证号", max_length=18)
	insured_address = models.CharField(u"参保地", max_length=200, blank=True)
	insured_month = models.DateField(u"参保月份")
	social_security_company = models.PositiveIntegerField(u"社保公司", null=True, blank=True)
	provident_fund_company = models.PositiveIntegerField(u"公积金公司", null=True, blank=True)
	company_month_sum = models.PositiveIntegerField(u"公司当月总合计", null=True, blank=True)
	social_security_person = models.PositiveIntegerField(u"社保个人", null=True, blank=True)
	provident_fund_person = models.PositiveIntegerField(u"公积金个人", null=True, blank=True)
	person_month_sum = models.PositiveIntegerField(u"个人当月合计", null=True, blank=True)
	social_security_pay_company = models.PositiveIntegerField(u"社保补缴公司", null=True, blank=True)
	social_security_pay_person = models.PositiveIntegerField(u"社保补缴个人", null=True, blank=True)
	provident_fund_pay_company = models.PositiveIntegerField(u"公积金补缴公司", null=True, blank=True)
	provident_fund_pay_person = models.PositiveIntegerField(u"公积金补缴个人", null=True, blank=True)
	penalty = models.PositiveIntegerField(u"滞纳金", null=True, blank=True)
	big_subsidy_refunds = models.PositiveIntegerField(u"大额补助退费", null=True, blank=True)
	social_security_refunds = models.PositiveIntegerField(u"社保退费", null=True, blank=True)
	provident_fund_refunds = models.PositiveIntegerField(u"公积金退费", null=True, blank=True)
	employers_liability_insurance = models.PositiveIntegerField(u"雇主责任险", null=True, blank=True)
	disablement_gold = models.PositiveIntegerField(u"残保金", null=True, blank=True)
	social_security_card_fees = models.PositiveIntegerField(u"社保卡费", null=True, blank=True)
	agency_fees_expenses = models.PositiveIntegerField(u"代理费(支付)", null=True, blank=True)
	agency_fees_revenue = models.PositiveIntegerField(u"代理费(收入)", null=True, blank=True)
	remarecruitment_fees = models.PositiveIntegerField(u"招聘费", null=True, blank=True)
	lump_sum = models.PositiveIntegerField(u"总额", null=True, blank=True)

	def __str__(self):
		return self.computer_number

	class Meta:
		verbose_name = u"社保明细"
		ordering = ['-id']  # id倒叙
		index_together = ["project_name", "name", "identity_card_number", "insured_month"]  # 索引字段组合
		permissions = (
			("browse_social_security_detail", u"浏览 增员信息"),
			("export_social_security_detail", u"导出 增员信息"),
		)

	def get_absolute_url(self):
		return "/social_security_detail/list"
