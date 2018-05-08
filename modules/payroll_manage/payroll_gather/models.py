# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models


class PayrollGater(models.Model):
	""" 薪资汇总 """

	class Meta:
		verbose_name = u"薪资汇总"
		permissions = (
			("browse_payrollgather", u"浏览 薪资汇总"),
			("export_payrollgather", u"导出 薪资汇总"),
		)

	def get_absolute_url(self):
		return reverse('payroll_manage:payroll_gather:payroll_gather_list')
