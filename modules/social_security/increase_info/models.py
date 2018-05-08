# coding=utf-8
from modules.dict_table.models import *
from modules.employee_management.employee_info.models import Employee

IS_VERIFY = (
	('1', u'未确认'),
	('2', u'确认'),
)


class Increase(models.Model):
	"""增员信息 """
	emplyid = models.ForeignKey(Employee, verbose_name=u"员工编号")
	dept_verify = models.CharField(u"部门确认", max_length=100, choices=IS_VERIFY, default="1")
	complete_verify = models.CharField(u"最终确认", max_length=100, choices=IS_VERIFY, default="1")
	remark = models.CharField(u"备注", max_length=200, blank=True)
	remark1 = models.CharField(u"备注1", max_length=256, blank=True)
	remark2 = models.CharField(u"备注2", max_length=256, blank=True)
	remark3 = models.CharField(u"备注3", max_length=256, blank=True)
	remark4 = models.CharField(u"备注4", max_length=256, blank=True)

	def __str__(self):
		return "Increase_" + self.emplyid.name

	class Meta:
		verbose_name = u"增员信息"
		ordering = ['-id']  # id倒叙
		index_together = ["emplyid"]  # 索引字段组合
		permissions = (
		("browse_increase", u"浏览 增员信息"),
		)

	def get_absolute_url(self):
		return "/increase/list"
