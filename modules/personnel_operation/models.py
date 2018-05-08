# coding=utf-8
from django.contrib.auth.models import User
from django.db import models

from modules.dict_table.models import ImproveStatus
from modules.organizational_structure.departments.models import Department
from modules.project_manage.models import Project

STATUS_CHOICES = (
	('1', u'是'),
	('2', u'否'),
)


class QualityAssurance(models.Model):
	"""质量管理 """
	INDEXENTRY = (
		('1', u'员工信息'),
		('2', u'合同'),
		('3', u'工资'),
		('4', u'社保'),
		('5', u'资料邮寄'),
		('6', u'发函'),
		('7', u'办卡资料'),
		('8', u'其他'),
	)

	department = models.ForeignKey(Department, verbose_name=u"服务部门", blank=True, null=True)
	project_id = models.ForeignKey(Project, verbose_name=u"项目名称", related_name="quality_project_name")
	index_items = models.CharField(u"指标项", max_length=1, choices=INDEXENTRY)
	problems_items = models.CharField(u"问题项", max_length=300)
	problems_explain = models.TextField(u"问题说明", max_length=300)
	error_number = models.PositiveIntegerField(u"操作错误数", default=1)
	provider = models.ForeignKey(User, verbose_name=u"数据提供者", related_name="quality_provider")
	error_date = models.DateField(u"问题日期")
	improve_time = models.PositiveIntegerField(u"改善时限", help_text=u"单位：天")
	improve_status = models.ForeignKey(ImproveStatus, verbose_name=u"改善状态")
	improve_date = models.DateField(u"改善日期")
	remark = models.CharField(u"备注", max_length=256, blank=True)
	create_user = models.ForeignKey(User, verbose_name=u"创建人", related_name="quality_create_user")
	create_date = models.DateTimeField(u"创建时间", auto_now_add=True)
	remark1 = models.CharField(u"备注1", max_length=256, blank=True)
	remark2 = models.CharField(u"备注2", max_length=256, blank=True)
	remark3 = models.CharField(u"备注3", max_length=256, blank=True)
	remark4 = models.CharField(u"备注4", max_length=256, blank=True)

	def __str__(self):
		return self.problems_items

	class Meta:
		verbose_name = u"个人操作质量"
		ordering = ['-id']  # id倒叙
		index_together = ["improve_status", "error_date"]  # 索引字段组合
		permissions = (
			("browse_qualityassurance", u"浏览 个人操作质量"),
		)
