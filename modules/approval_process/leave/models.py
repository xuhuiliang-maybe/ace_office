# coding=utf-8
import traceback
from django.db import models
from modules.approval_process.models import Public
from modules.approval_process.models import PendingApproval  # 待审批
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from modules.dict_table.models import *

LEAVE_TYPE = (
	("1", u"年假"),
	("2", u"病假"),
	("3", u"事假"),
	("4", u"婚假"),
	("5", u"产假"),
	("6", u"丧假"),
)


class Leave(Public):
	""" 请假表 """
	handle_user = models.ForeignKey(User, verbose_name=u"审批人", related_name="leave_handle_user", blank=True,
					null=True)
	apply_user = models.ForeignKey(User, verbose_name=u"申请人", related_name="leave_apply_user")
	begin_date = models.DateField(u"请假起始时间")  # 开始时间
	end_date = models.DateField(u"请假终止时间")  # 结束时间
	leave_type = models.ManyToManyField(LeaveType, verbose_name=u"请假类型", blank=True,
							    help_text=u"按住 ”Control“，或者Mac上的 “Command”，可以选择多个。")

	def __str__(self):
		return self.title + "-" + self.note

	class Meta:
		verbose_name = u"请假"
		ordering = ['-id']  # id倒叙
		index_together = ["title", "apply_user"]  # 索引字段组合
		permissions = (
			("browse_leave", u"浏览 请假"),
		)


@receiver(post_save, sender=Leave)  # 信号的名字，发送者
def add_leave_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	"""增加 请假 申请事件 """
	try:
		pend_obj = PendingApproval.objects.filter(object_id=instance.id, apply_type="1")
		if not pend_obj.exists():
			PendingApproval(event=instance, apply_type="1").save()
	except:
		traceback.print_exc()
