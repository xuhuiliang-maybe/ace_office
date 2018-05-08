# coding=utf-8
import traceback
from django.db import models
from modules.approval_process.models import Public
from modules.approval_process.models import PendingApproval  # 待审批
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from modules.project_manage.models import Project
from modules.dict_table.models import Subject
from modules.organizational_structure.departments.models import Department

IS_BILLING = (
	('1', u'是'),
	('2', u'否'),
)

COST_SHARING_CHOICE = (
	("1", u"项目分摊"),
	("2", u"个人分摊"),
	("3", u"部门分摊"),
	("4", u"公司分摊"),
)


class RecruitedBilling(Public):
	""" 待招结算与开票 """
	handle_user = models.ForeignKey(User, verbose_name=u"审批人", related_name="recruitedbilling_handle_user",
					blank=True,
					null=True)
	apply_user = models.ForeignKey(User, verbose_name=u"申请人", related_name="recruitedbilling_apply_user")

	project_name = models.ForeignKey(Project, verbose_name=u"项目名称", null=True)
	billing_month = models.DateField(u"结算月份", blank=True, null=True)
	settlement_amount = models.PositiveIntegerField(u"结算金额", blank=True, null=True)
	is_billing = models.CharField(u"是否开票", choices=IS_BILLING, max_length=1, blank=True, null=True)
	content = models.CharField(u"说明", max_length=255, blank=True, null=True)

	def __str__(self):
		return self.title + "-" + self.note

	class Meta:
		verbose_name = u"待招结算与开票"
		ordering = ['-id']  # id倒叙
		index_together = ["title", "apply_user"]  # 索引字段组合
		permissions = (
			("browse_recruited_billing", u"浏览 待招结算与开票"),
		)


@receiver(post_save, sender=RecruitedBilling)  # 信号的名字，发送者
def add_recruitedbilling_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	"""增加 待招结算与开票 申请事件 """
	try:
		pend_obj = PendingApproval.objects.filter(object_id=instance.id, apply_type="9")
		if not pend_obj.exists():
			PendingApproval(event=instance, apply_type="9").save()
	except:
		traceback.print_exc()


class RecruitedBillingDetails(models.Model):
	"""待招结算与开票，报销/销账明细表"""
	applicants = models.ForeignKey(RecruitedBilling, verbose_name=u"待招结算与开票申请", editable=False,
				       related_name="RecruitedBillingDetails")
	dates = models.DateField(u"日期", blank=True, null=True)
	money = models.PositiveIntegerField(u"金额", blank=True, null=True)
	subject = models.ForeignKey(Subject, verbose_name=u"科目")
	cost_sharing = models.CharField(u"费用分摊方式", max_length=1, choices=COST_SHARING_CHOICE)
	cost_obj = models.CharField(u"费用分摊对象", max_length=255, blank=True, null=True)
	cost_detail_content = models.CharField(u"费用明细说明", max_length=255, blank=True, null=True)
	invoice_state = models.CharField(u"发票情况", max_length=255, blank=True, null=True)
	payee = models.ForeignKey(User, verbose_name=u"领款人", related_name="recruitedbillingdetails_payee")

	def __str__(self):
		return str(self.dates)

	class Meta:
		verbose_name = u"待招结算与开票-报销/销账明细表"
		permissions = (
			("browse_recruitedbillingdetails", u"浏览 待招结算与开票-报销/销账明细表"),
		)
