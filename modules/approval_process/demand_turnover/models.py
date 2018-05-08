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


class DemandTurnover(Public):
	""" 管理人员需求与离职 """
	handle_user = models.ForeignKey(User, verbose_name=u"审批人", related_name="demand_turnover_handle_user",
					blank=True,
					null=True)
	apply_user = models.ForeignKey(User, verbose_name=u"申请人", related_name="demand_turnover_apply_user")

	def __str__(self):
		return self.title + "-" + self.note

	class Meta:
		verbose_name = u"管理人员需求与离职"
		ordering = ['-id']  # id倒叙
		index_together = ["title", "apply_user"]  # 索引字段组合
		permissions = (
			("browse_demand_turnover", u"浏览 管理人员需求与离职"),
		)


@receiver(post_save, sender=DemandTurnover)  # 信号的名字，发送者
def add_demand_turnover_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	"""增加 管理人员需求与离职 申请事件 """
	try:
		pend_obj = PendingApproval.objects.filter(object_id=instance.id, apply_type="7")
		if not pend_obj.exists():
			PendingApproval(event=instance, apply_type="7").save()
	except:
		traceback.print_exc()
