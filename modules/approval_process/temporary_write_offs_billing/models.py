# coding=utf-8
import traceback
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from modules.approval_process.models import Public
from modules.approval_process.models import PendingApproval
from modules.organizational_structure.departments.models import Department
from modules.project_manage.models import Project
from modules.employee_management.employee_info.models import GENDER_CHOICES

BILLING_TYPE = (
	('1', u'单独结算'),
	('2', u'合并结算'),
)

IS_BILLING = (
	('1', u'是'),
	('2', u'否'),
)


class TemporaryWriteOffsBilling(Public):
	""" 临时工销账与开票 """
	handle_user = models.ForeignKey(User, verbose_name=u"审批人",
					related_name="temporary_write_offs_billing_handle_user",
					blank=True,
					null=True)
	apply_user = models.ForeignKey(User, verbose_name=u"申请人",
				       related_name="temporary_write_offs_billing_apply_user")

	billing_month = models.DateField(u"结算月份", blank=True, null=True)
	project_name = models.ForeignKey(Project, verbose_name=u"项目名称", null=True)
	billing_date_start = models.DateField(u"结算周期起始", blank=True, null=True)
	billing_date_end = models.DateField(u"结算周期终止", blank=True, null=True)
	billing_content = models.CharField(u"结算内容", max_length=255, blank=True, null=True)
	billing_type = models.CharField(u"结算方式", max_length=1, choices=BILLING_TYPE, blank=True, null=True)

	main_business_income = models.PositiveIntegerField(u"主营业收入", editable=False, blank=True, null=True)  # 自动计算
	management_fee = models.PositiveIntegerField(u"管理费", blank=True, null=True)
	wage_receive = models.PositiveIntegerField(u"工资(收)", blank=True, null=True)
	shuttle_fee_receive = models.PositiveIntegerField(u"班车费(收)", blank=True, null=True)
	meals_receive = models.PositiveIntegerField(u"餐费(收)", blank=True, null=True)
	dormitory_fee_receive = models.PositiveIntegerField(u"宿舍费(收)", blank=True, null=True)
	daily_receive = models.PositiveIntegerField(u"商报(收)", blank=True, null=True)
	compensate_reparation_receive = models.PositiveIntegerField(u"赔付款(收)", blank=True, null=True)

	actual_outlay = models.PositiveIntegerField(u"实际支出", blank=True, null=True)
	main_business_outlay = models.PositiveIntegerField(u"主营业支出", blank=True, null=True)  # 自动计算
	wage_outlay = models.PositiveIntegerField(u"工资(付)", blank=True, null=True)
	shuttle_fee_outlay = models.PositiveIntegerField(u"班车费(付)", blank=True, null=True)
	meals_outlay = models.PositiveIntegerField(u"餐费(付)", blank=True, null=True)
	daily_outlay = models.PositiveIntegerField(u"商报(付)", blank=True, null=True)
	compensate_reparation_outlay = models.PositiveIntegerField(u"赔偿/补偿金(付)", blank=True, null=True)
	borrow_loan = models.PositiveIntegerField(u"已借备用金", blank=True, null=True)

	# 公式=已借备用金-主营业务支出，结果如果是正数，自动显示出：应返还公司XX钱；如果是负数，自动显示：公司应支付XX钱
	difference = models.PositiveIntegerField(u"差额", default=0, editable=False)
	is_billing = models.CharField(u"是否开票", choices=IS_BILLING, max_length=1, blank=True, null=True)

	def __str__(self):
		return self.title + "-" + self.note

	class Meta:
		verbose_name = u"临时工销账与开票"
		ordering = ['-id']  # id倒叙
		index_together = ["title", "apply_user"]  # 索引字段组合
		permissions = (
			("browse_temporary_write_offs_billing", u"浏览 临时工销账与开票"),
		)


@receiver(post_save, sender=TemporaryWriteOffsBilling)  # 信号的名字，发送者
def add_temporary_write_offs_billing_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	"""增加 临时工销账与开票 申请事件 """
	try:
		pend_obj = PendingApproval.objects.filter(object_id=instance.id, apply_type="8")
		if not pend_obj.exists():
			PendingApproval(event=instance, apply_type="8").save()
	except:
		traceback.print_exc()


# 临时工销账与开票-明细
class TemporaryWriteOffsBillingDetails(models.Model):
	applicants = models.ForeignKey(TemporaryWriteOffsBilling, verbose_name=u"临时工销账与开票申请", editable=False,
				       related_name="temporarywriteoffsbillingdetails")

	# 临时工相关字段
	name = models.CharField(u"姓名", max_length=100)
	sex = models.CharField(u"性别", max_length=2, choices=GENDER_CHOICES, blank=True, help_text=u"选填，可由身份证号计算")
	identity_card_number = models.CharField(u"身份证号", max_length=18)
	project_name = models.ForeignKey(Project, verbose_name=u"项目名称", blank=True, null=True, related_name="temporary")
	recruitment_attache = models.ForeignKey(User, blank=True, null=True, verbose_name=u"招聘人员",
						related_name="temporary_user_recruitment_attache")
	phone_number = models.CharField(u"联系电话", max_length=100, blank=True)
	start_work_date = models.DateField(u"开始工作日", blank=True, null=True)
	end_work_date = models.DateField(u"结束工作日", blank=True, null=True)
	work_days = models.PositiveIntegerField(u"工作天数", blank=True, null=True)
	hours = models.PositiveIntegerField(u"小时数", blank=True, null=True)
	amount_of_payment = models.PositiveIntegerField(u"发放金额", blank=True, null=True)
	release_user = models.ForeignKey(User, blank=True, null=True, verbose_name=u"发放人",
					 related_name="temporary_release_user")
	release_time = models.DateField(u"发放时间", blank=True, null=True)
	remark1 = models.CharField(u"备注1", max_length=256, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"临时工销账与开票明细"
