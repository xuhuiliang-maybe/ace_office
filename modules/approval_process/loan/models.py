# coding=utf-8
import traceback
from django.db import models
from modules.approval_process.models import Public
from modules.approval_process.models import PendingApproval  # 待审批
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Loan(Public):
	""" 借款 """
	handle_user = models.ForeignKey(User, verbose_name=u"审批人", related_name="loan_handle_user", blank=True,
					null=True)
	apply_user = models.ForeignKey(User, verbose_name=u"申请人", related_name="loan_apply_user")
	money = models.PositiveIntegerField(u"申请金额", default=0, help_text=u"申请备用金具体金额")
	borrowing_date = models.DateField(u"借款日", help_text=u"能拿到备用金时间")
	repayment_date = models.DateField(u"还款日")

	def __str__(self):
		return self.title + "-" + self.note

	class Meta:
		verbose_name = u"备用金"
		ordering = ['-id']  # id倒叙
		index_together = ["title", "apply_user"]  # 索引字段组合
		permissions = (
			("browse_loan", u"浏览 备用金"),
		)


@receiver(post_save, sender=Loan)  # 信号的名字，发送者
def add_loan_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	"""增加 借款 申请事件 """
	try:
		pend_obj = PendingApproval.objects.filter(object_id=instance.id, apply_type="2")
		if not pend_obj.exists():
			PendingApproval(event=instance, apply_type="2").save()

		from modules.finance.loans_and_write_offs.models import LoansAndWriteOffs
		LoansAndWriteOffs(loan=instance).save()
	except:
		traceback.print_exc()


class LoanBudgetDetails(models.Model):
	"""备用金，费用预算明细"""
	applicants = models.ForeignKey(Loan, verbose_name=u"备用金申请", editable=False, related_name="LoanBudgetDetails")

	# 临时工预算明细
	date_range = models.CharField(u"日期", max_length=256, help_text=u"临时工预算明细")
	days = models.PositiveIntegerField(u"天数", default=0)
	daily_number = models.PositiveIntegerField(u"每天人数", default=0)
	hours_per_day = models.PositiveIntegerField(u"每天人均工时", default=0)
	hourly_wage = models.PositiveIntegerField(u"小时工资", default=0)
	meals_per_capita = models.PositiveIntegerField(u"人均餐费", default=0)
	traffic_fee = models.PositiveIntegerField(u"交通费", default=0)
	# 天数*每天人数*每天人均工时*小时工资+人均餐费*每天人数+交通费
	temporary_total = models.PositiveIntegerField(u"临时工预算合计", default=0, editable=False)

	# 其他预算明细
	amount = models.PositiveIntegerField(u"数量", default=0, help_text=u"其他预算明细")
	unit_price = models.PositiveIntegerField(u"单价", default=0)
	other_total = models.PositiveIntegerField(u"其他预算合计", default=0, editable=False)  # 数量*单价

	# 总计
	all_total = models.PositiveIntegerField(u"总计", default=0, editable=False, help_text=u"其他预算明细")  # 其他预算合计+临时工预算合计

	def __str__(self):
		return self.date_range

	class Meta:
		verbose_name = u"备用金费用预算明细"
