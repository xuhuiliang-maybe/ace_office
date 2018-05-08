# coding=utf-8
import traceback

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from modules.employee_management.employee_info.models import Employee
from modules.organizational_structure.departments.models import Department
from modules.project_manage.models import Project

APPLY_STATUS_CHOICES = (
	('1', u'待审批'),
	('2', u'通过'),
	('3', u'拒绝'),
)

APPLY_TYPE_CHOICES = (
	('1', u'请假'),
	('2', u'备用金'),
	('3', u'报销与销账'),
	('4', u'工资与职位调整'),
	('5', u'工资补发申请'),
	('6', u'结算与发薪'),
	('7', u'管理人员需求与离职'),
	('8', u'临时工销账与开票'),
	('9', u'待招结算与销账'),
)


class Public(models.Model):
	"""申请模型公用基类 """

	title = models.CharField(u"申请标题", max_length=100)
	note = models.TextField(u"申请说明", max_length=256)
	created = models.DateTimeField(u"申请时间", auto_now_add=True)
	handle_date = models.DateTimeField(u"审批时间", blank=True, null=True)
	reason = models.CharField(u"审批回复", max_length=100, blank=True)
	status = models.CharField(u"审批状态", max_length=1, choices=APPLY_STATUS_CHOICES, default='1')
	apply_types = models.CharField(u"申请类型", max_length=1, choices=APPLY_TYPE_CHOICES, null=True)
	remark1 = models.CharField(u"备注1", max_length=256, blank=True)
	remark2 = models.CharField(u"备注2", max_length=256, blank=True)
	pending_approvals = generic.GenericRelation('PendingApproval')  # 当一个Model实例被删除时，PendingApproval中的相关记录也就会被删除。

	class Meta:
		abstract = True
		ordering = ["-created"]
		permissions = (

		)

	def check_permission(self, handle_user):
		"""校验审批权限
		:param handle_user:审批人
		:return:
		"""
		try:
			if handle_user == self.apply_user:
				return False
			if self.apply_types == "1":  # 请假
				approval_days = handle_user.authorize_leave
				user_leave_days = self.end_date - self.begin_date
				if approval_days < user_leave_days.days:
					return False
			elif self.apply_types == "2":  # 备用金，借款
				approval_money = handle_user.authorize_loan
				if approval_money < self.money:
					return False
			elif self.apply_types == "4":  # 工资，与职位调整
				approval_money = handle_user.authorize_wage
				if approval_money < self.money:
					return False
			return True
		except:
			traceback.print_exc()

	def agree_apply(self, handle_user):
		try:
			# 判断权限
			self.status = "2"
			self.handle_user = handle_user
			self.handle_date = timezone.now()
			self.save()

			applicants_model = self._meta.object_name  # 当前审批申请模型名称

			if applicants_model == "TemporaryWriteOffsBilling":
				return self.add_temporary_info()

			return u"成功审批"
		except:
			traceback.print_exc()
			return u"审批异常"

	def add_temporary_info(self):
		# 临时工销账与开票，审核通过，将明细中临时工信息添加到临时工信息中
		from modules.approval_process.temporary_write_offs_billing.models import \
			TemporaryWriteOffsBillingDetails
		try:
			detail_list = TemporaryWriteOffsBillingDetails.objects.filter(applicants=self)
			if detail_list.exists():
				for one_info in detail_list:
					user_obj = Employee()
					user_obj.name = one_info.name
					user_obj.sex = one_info.sex
					user_obj.identity_card_number = one_info.identity_card_number
					user_obj.project_name = one_info.project_name
					if one_info.recruitment_attache:
						user_obj.recruitment_attache = one_info.recruitment_attache
					user_obj.is_temporary = True
					user_obj.phone_number = one_info.phone_number
					user_obj.start_work_date = one_info.start_work_date
					user_obj.end_work_date = one_info.end_work_date
					user_obj.work_days = one_info.work_days
					user_obj.hours = one_info.hours
					user_obj.amount_of_payment = one_info.amount_of_payment
					if one_info.release_user:
						user_obj.release_user = one_info.release_user
					user_obj.release_time = one_info.release_time
					user_obj.remark1 = one_info.remark1
					user_obj.save()
			return u"成功审批，临时工创建成功！"
		except:
			traceback.print_exc()
			return u"审批成功，临时工创建异常！"

	def refuse_apply(self, handle_user, reason):
		try:
			self.status = "3"
			self.reason = reason
			self.handle_user = handle_user
			self.handle_date = timezone.now()
			self.save()
			return u"成功审批"
		except:
			traceback.print_exc()


class PendingApproval(models.Model):
	""" 待审批信息, 审批事件 """
	content_type = models.ForeignKey(ContentType)  # 任意一个Model
	object_id = models.PositiveIntegerField()  # 通过这个字段得到实例
	event = generic.GenericForeignKey('content_type', 'object_id')
	apply_type = models.CharField(u"申请类型", max_length=1, choices=APPLY_TYPE_CHOICES, null=True)

	class Meta:
		verbose_name = u"待审批申请信息"
		ordering = ['-id']  # id倒叙
		permissions = (
			("browse_pendingapproval", u"浏览 待审批信息"),
		)
