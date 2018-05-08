# coding=utf-8
from django.db import models
from modules.approval_process.loan.models import Loan


# 借款与销账
class LoansAndWriteOffs(models.Model):
	loan = models.ForeignKey(Loan, verbose_name=u"备用金", related_name="loansandwriteoffs", blank=True, null=True)
	amount_write_offs = models.PositiveIntegerField(u"销账金额", blank=True, null=True)
	write_offs_date = models.DateField(u"销账时间", blank=True, null=True)
	remark = models.CharField(u"备注", max_length=256, blank=True, null=True)

	def __str__(self):
		return self.remark

	class Meta:
		verbose_name = u"借款与销账"
		ordering = ['-id']  # id倒叙
		permissions = (
			("browse_loansandwriteoffs", "浏览 借款与销账"),
			("export_loansandwriteoffs", "导出 借款与销账"),
		)
