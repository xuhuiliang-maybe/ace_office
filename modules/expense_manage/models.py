# coding=utf-8

from django.contrib.auth.models import User
from django.db import models

from modules.dict_table.models import ExpenseType
from modules.employee_management.employee_info.models import Employee
from modules.project_manage.models import Project

APPLY_STATUS_CHOICES = (
('1', u'待审批'),
('2', u'通过'),
('3', u'拒绝'),
)

INOROUT_CHOICES = (
('1', u'支出'),
('2', u'收入'),
)


class Expense(models.Model):
	"""费用信息 """
	emplyid = models.ForeignKey(Employee, verbose_name=u"员工编号", related_name="expense_emp", blank=True, null=True)
	projectid = models.ForeignKey(Project, verbose_name=u"项目名称", related_name="expense_project", blank=True,
	                              null=True)
	userid = models.ForeignKey(User, verbose_name=u"费用负责人", related_name="expense_user", blank=True, null=True)
	expensetype = models.ForeignKey(ExpenseType, verbose_name=u"费用类型", blank=True, null=True)
	inorout = models.CharField(u"收支类型", max_length=100, choices=INOROUT_CHOICES, default='1')
	note = models.CharField(u"申请说明", max_length=100)
	apply_user = models.ForeignKey(User, verbose_name=u"申请人")
	created = models.DateTimeField(u"申请时间", auto_now_add=True)
	handle_user = models.CharField(u"审批人", max_length=100, blank=True)
	handle_date = models.DateTimeField(u"审批时间", blank=True, null=True)
	reason = models.CharField(u"审批回复", max_length=100, blank=True)
	status = models.CharField(u"审批状态", max_length=100, choices=APPLY_STATUS_CHOICES, default='1')
	remark1 = models.CharField(u"备注1", max_length=256, blank=True)
	remark2 = models.CharField(u"备注2", max_length=256, blank=True)
	remark3 = models.CharField(u"备注3", max_length=256, blank=True)
	remark4 = models.CharField(u"备注4", max_length=256, blank=True)
	remark5 = models.CharField(u"备注5", max_length=256, blank=True)

	def __str__(self):
		return self.emplyid

	class Meta:
		verbose_name = u"费用信息"
		ordering = ['-id']  # id倒叙
		index_together = ["emplyid", "projectid"]  # 索引字段组合
		permissions = (
		("browse_expense", u"浏览 费用信息"),
		)

	def get_absolute_url(self):
		return "/expense/list"
