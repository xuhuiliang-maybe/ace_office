# coding=utf-8
from django.db import models
from modules.approval_process.models import Public
from modules.approval_process.models import PendingApproval
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import traceback


class Wage(Public):
	""" 工资与职位调整申请表 """
	handle_user = models.ForeignKey(User, verbose_name=u"审批人", related_name="wage_handle_user", blank=True, null=True)
	apply_user = models.ForeignKey(User, verbose_name=u"申请人", related_name="wage_apply_user")
	money = models.PositiveIntegerField(u"金额", default=0)

	def __str__(self):
		return self.title + "-" + self.note

	class Meta:
		verbose_name = u"工资与职位调整"
		ordering = ['-id']  # id倒叙
		index_together = ["title", "apply_user"]  # 索引字段组合
		permissions = (
			("browse_wage", u"浏览 工资与职位调整"),
		)


@receiver(post_save, sender=Wage)  # 信号的名字，发送者
def add_wage_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	"""增加 工资 申请事件 """
	try:
		pend_obj = PendingApproval.objects.filter(object_id=instance.id, apply_type="4")
		if not pend_obj.exists():
			PendingApproval(event=instance, apply_type="4").save()
	except:
		traceback.print_exc()
