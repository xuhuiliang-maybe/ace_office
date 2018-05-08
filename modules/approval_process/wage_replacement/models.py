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


class WageReplacement(Public):
	""" 工资补发申请 """
	handle_user = models.ForeignKey(User, verbose_name=u"审批人", related_name="wage_replacement_handle_user",
					blank=True,
					null=True)
	apply_user = models.ForeignKey(User, verbose_name=u"申请人", related_name="wage_replacement_apply_user")

	def __str__(self):
		return self.title + "-" + self.note

	class Meta:
		verbose_name = u"工资补发申请"
		ordering = ['-id']  # id倒叙
		index_together = ["title", "apply_user"]  # 索引字段组合
		permissions = (
			("browse_wage_replacement", u"浏览 工资补发申请"),
		)


@receiver(post_save, sender=WageReplacement)  # 信号的名字，发送者
def add_wage_replacement_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	"""增加 工资补发申请 申请事件 """
	try:
		pend_obj = PendingApproval.objects.filter(object_id=instance.id, apply_type="5")
		if not pend_obj.exists():
			PendingApproval(event=instance, apply_type="5").save()
	except:
		traceback.print_exc()


PAYMENT_UNIT = (
	('1', u'邦泰'),
	('2', u'杰博'),
)


class WageReplacementDetails(models.Model):
	"""补发明细 """
	applicants = models.ForeignKey(WageReplacement, verbose_name=u"工资补发申请", editable=False,
				       related_name="WageReplacementDetails")

	payment_unit = models.CharField(u"付款单位", max_length=1, choices=PAYMENT_UNIT)
	department = models.ForeignKey(Department, verbose_name=u"服务部门")
	project_name = models.ForeignKey(Project, verbose_name=u"项目名称")
	name = models.CharField(u"姓名", max_length=256)
	identity_card_number = models.CharField(u"身份证号", max_length=18)
	salary_card_number = models.CharField(u"银行卡号", max_length=100, blank=True)
	bank_account = models.CharField(u"开户银行", max_length=100, blank=True)
	replacement_money = models.PositiveIntegerField(u"补发金额")
	cost_month = models.DateField(u"费用月份")
	replacement_type = models.CharField(u"补发类型", max_length=256)
	replacement_explain = models.CharField(u"补发说明", max_length=256)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"补发明细"
