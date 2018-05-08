# coding=utf-8
from django.db import models

from modules.employee_management.employee_info.models import Employee


class Payroll(models.Model):
	""" 结算发薪 """
	employee = models.ForeignKey(Employee, verbose_name=u"员工编号")
	pay_month = models.DateField(u"工资月份", blank=True, null=True)
	post_salary = models.FloatField(u"岗位工资", blank=True, null=True)
	float_salary = models.FloatField(u"浮动工资", blank=True, null=True)
	full_award = models.FloatField(u"全勤奖", blank=True, null=True)
	award = models.FloatField(u"奖金", blank=True, null=True)
	hous_subsidy = models.FloatField(u"住房补贴", blank=True, null=True)
	traffic_subsidy = models.FloatField(u"交通补贴", blank=True, null=True)
	commodity_subsidy = models.FloatField(u"物价补贴", blank=True, null=True)
	food_subsidy = models.FloatField(u"伙食补贴", blank=True, null=True)
	time_salary = models.FloatField(u"计时工资", blank=True, null=True)
	piece_salary = models.FloatField(u"计件工资", blank=True, null=True)
	deducty_salary = models.FloatField(u"应扣工资", blank=True, null=True)
	remark1 = models.CharField(u"备注1", max_length=256, blank=True)
	remark2 = models.CharField(u"备注2", max_length=256, blank=True)
	remark3 = models.CharField(u"备注3", max_length=256, blank=True)
	remark4 = models.CharField(u"备注4", max_length=256, blank=True)
	remark5 = models.CharField(u"备注5", max_length=256, blank=True)

	def __str__(self):
		return self.employee

	class Meta:
		verbose_name = u"结算发薪"
		ordering = ['-id']  # id倒叙
		index_together = ["employee", "pay_month"]  # 索引字段组合
		permissions = (
			("browse_payroll", u"浏览 结算发薪"),
		)
