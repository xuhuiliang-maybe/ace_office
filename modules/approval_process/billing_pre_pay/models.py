# coding=utf-8
from django.db import models
from modules.approval_process.models import Public
from modules.approval_process.models import PendingApproval
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import traceback
from modules.organizational_structure.departments.models import Department
from modules.project_manage.models import Project


class BillingPrePay(Public):
	""" 结算与发薪 """
	handle_user = models.ForeignKey(User, verbose_name=u"审批人", related_name="billing_pre_pay_handle_user",
					blank=True,
					null=True)
	apply_user = models.ForeignKey(User, verbose_name=u"申请人", related_name="billing_pre_pay_apply_user")

	billingprepay_month = models.DateField(u"结算与发薪月份")
	project_name = models.ForeignKey(Project, verbose_name=u"结算项目名称")

	billing_date_start = models.DateField(u"结算周期起始", blank=True, null=True)
	billing_date_end = models.DateField(u"结算周期终止", blank=True, null=True)
	billing_content = models.CharField(u"结算内容", max_length=255, blank=True, null=True)

	main_business_income = models.PositiveIntegerField(u"主营业收入", editable=False, blank=True, null=True)  # 自动计算
	management_fee = models.PositiveIntegerField(u"管理费", blank=True, null=True)
	wage_receive = models.PositiveIntegerField(u"工资(收)", blank=True, null=True)
	social_security_receive = models.PositiveIntegerField(u"社保(收)", blank=True, null=True)
	provident_fund_receive = models.PositiveIntegerField(u"公积金(收)", blank=True, null=True)
	union_fee_receive = models.PositiveIntegerField(u"工会费(收)", blank=True, null=True)
	disablement_gold = models.PositiveIntegerField(u"残保金", blank=True, null=True)
	shuttle_fee_receive = models.PositiveIntegerField(u"班车费(收)", blank=True, null=True)
	meals_receive = models.PositiveIntegerField(u"餐费(收)", blank=True, null=True)
	dormitory_fee_receive = models.PositiveIntegerField(u"宿舍费(收)", blank=True, null=True)
	daily_receive = models.PositiveIntegerField(u"商报(收)", blank=True, null=True)
	compensate_reparation_receive = models.PositiveIntegerField(u"偿/赔偿金(收)", blank=True, null=True)
	bonus_receive = models.PositiveIntegerField(u"奖金类(收)", blank=True, null=True)
	other_receive = models.PositiveIntegerField(u"其他收入", blank=True, null=True)

	grant_total = models.PositiveIntegerField(u"发放总额", editable=False, blank=True, null=True)  # 自动计算
	ccb = models.PositiveIntegerField(u"建行", blank=True, null=True)
	merchants_bank = models.PositiveIntegerField(u"招行", blank=True, null=True)
	icbc = models.PositiveIntegerField(u"工行", blank=True, null=True)
	other_bank = models.PositiveIntegerField(u"其他银行", blank=True, null=True)

	# billing_detail = models.CharField(u"结算明细", max_length=256, null=True, blank=True)
	# pay_batch = models.CharField(u"发薪批次", max_length=256)
	# pay_lump_sum = models.PositiveIntegerField(u"发薪总额")
	# pay_bank_detail = models.CharField(u"发薪银行明细", max_length=256)
	# pay_time = models.CharField(u"发薪时间", max_length=256)

	def __str__(self):
		return self.title + "-" + self.note

	class Meta:
		verbose_name = u"结算与发薪"
		ordering = ['-id']  # id倒叙
		index_together = ["title", "apply_user"]  # 索引字段组合
		permissions = (
			("browse_billingprepay", u"浏览 结算与发薪"),
		)


@receiver(post_save, sender=BillingPrePay)  # 信号的名字，发送者
def add_billing_pre_pay_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	"""增加 结算与发薪 申请事件 """
	try:
		pend_obj = PendingApproval.objects.filter(object_id=instance.id, apply_type="6")
		if not pend_obj.exists():
			PendingApproval(event=instance, apply_type="6").save()
	except:
		traceback.print_exc()
