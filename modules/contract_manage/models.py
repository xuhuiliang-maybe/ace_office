# coding=utf-8
from django.contrib.auth.models import User
from django.db import models

from modules.employee_management.employee_info.models import GENDER_CHOICES, NATION_CHOICES
from modules.project_manage.models import Project

# 合同期限
DEADLINE = (
	('1', u'24个月'),
	('2', u'36个月'),
)

# 试用期
PROBATION = (
	('1', u'2个月'),
	('2', u'6个月'),
)

# 发放方式
PAYROLL_GRANT = (
	('1', u'银行打卡'),
	('2', u'现金'),
)


class Contract(models.Model):
	project_name = models.ForeignKey(Project, verbose_name=u"项目名称")
	name = models.CharField(u"姓名", max_length=100)
	identity_card_number = models.CharField(u"身份证号", max_length=18)
	sex = models.CharField(u"性别", max_length=2, choices=GENDER_CHOICES, blank=True)
	birthday = models.DateField(u"出生年月", blank=True, null=True)
	nation = models.CharField(u"民族", max_length=2, choices=NATION_CHOICES, blank=True)
	address = models.CharField(u"住址", max_length=255, blank=True)
	phone_number = models.CharField(u"联系电话", max_length=100, blank=True)
	receive_address = models.CharField(u"指定通知接收地址", max_length=255, blank=True, help_text=u"选填，默认为住址信息")
	emergency_contact_name = models.CharField(u"紧急联系人姓名", max_length=100, blank=True)
	emergency_contact_phone = models.CharField(u"紧急联系人电话", max_length=100, blank=True)

	# 合同期限
	start_date = models.DateField(u"合同开始时间", blank=True, null=True)
	end_date = models.DateField(u"合同结束时间", blank=True, null=True)
	deadline = models.CharField(u"合同期限", max_length=1, choices=DEADLINE, blank=True)
	probation = models.CharField(u"试用期", max_length=1, choices=PROBATION, blank=True)  # 合同2年，试用期2个月，合同3年，试用期6个月

	workplace = models.CharField(u"工作地点", max_length=255, blank=True)
	post = models.CharField(u"岗位", max_length=255, blank=True)

	payroll_standard = models.CharField(u"薪资标准", max_length=255, blank=True)
	payroll_grant = models.CharField(u"发薪方式", max_length=1, choices=PAYROLL_GRANT, blank=True)
	grant_date = models.CharField(u"发薪时间", max_length=255, blank=True, default=u"次月月底前")

	remark = models.CharField(u"备注", max_length=256, blank=True)
	download_times = models.PositiveIntegerField(u"下载次数", default=0)

	def __str__(self):
		return self.name + "--" + self.identity_card_number

	class Meta:
		abstract = True


# 派遣
class ContractSend(Contract):
	# 派遣单位：根据项目名称对应的客户名称
	start_send_deadline = models.DateField(u"派遣期限开始", blank=True, null=True, help_text=u"默认为合同开始时间")
	end_send_deadline = models.DateField(u"派遣期限结束", blank=True, null=True)

	class Meta:
		verbose_name = u"合同签订-派遣"
		ordering = ['-id']  # id倒叙
		permissions = (
			("browse_contractsend", u"浏览 合同签订-派遣"),
		)


# 外包
class ContractOutsourc(Contract):
	class Meta:
		verbose_name = u"合同签订-外包"
		ordering = ['-id']  # id倒叙
		permissions = (
			("browse_contractoutsourc", u"浏览 合同签订-外包"),
		)


# 实习生
class ContractIntern(Contract):
	class Meta:
		verbose_name = u"合同签订-实习生"
		ordering = ['-id']  # id倒叙
		permissions = (
			("browse_contractintern", u"浏览 合同签订-实习生"),
		)


# 劳务
class ContractService(Contract):
	class Meta:
		verbose_name = u"合同签订-劳务"
		ordering = ['-id']  # id倒叙
		permissions = (
			("browse_contractservice", u"浏览 合同签订-劳务"),
		)


# 小时工
class ContractHourly(Contract):
	project_date = models.DateField(u"项目时间", blank=True)
	start_work_date = models.DateField(u"开始工作日", blank=True, null=True)
	end_work_date = models.DateField(u"结束工作日", blank=True, null=True)
	work_days = models.PositiveIntegerField(u"工作天数", blank=True, null=True)
	work_hours = models.PositiveIntegerField(u"小时数", blank=True, null=True)
	grant_money = models.PositiveIntegerField(u"发放金额", blank=True, null=True)
	recipients = models.CharField(u"领取人", max_length=255, blank=True)
	grant_user = models.ForeignKey(User, verbose_name=u"发放人", related_name="grant_user", blank=True, null=True)
	grant_time = models.DateField(u"发放时间", blank=True, null=True)
	recruiters = models.ForeignKey(User, verbose_name=u"招聘人", related_name="recruiters", blank=True, null=True)

	class Meta:
		verbose_name = u"合同签订-小时工"
		ordering = ['-id']  # id倒叙
		permissions = (
			("browse_contracthourly", u"浏览 合同签订-小时工"),
		)


# 合同类型
CONTRACT_TYPE = (
	('1', u'派遣'),
	('2', u'外包'),
	('3', u'实习生'),
	('4', u'劳务'),
	('5', u'小时工'),
)
CONTRACT_DICT = {
	"1": ContractSend,
	"2": ContractOutsourc,
	"3": ContractIntern,
	"4": ContractService,
	"5": ContractHourly,
}


# 合同预览
class ContractPreviewCode(models.Model):
	contract_type = models.CharField(u"合同类型", max_length=1, choices=CONTRACT_TYPE)
	code = models.CharField(u"预览码", max_length=6)
	end_time = models.DateTimeField(u"有效终止时间")
	number = models.CharField(u"预览次数", max_length=100, default=0)
	generate_user = models.ForeignKey(User, verbose_name=u"生成者", null=True, blank=True)

	def __str__(self):
		return self.code

	class Meta:
		verbose_name = u"合同预览"
		verbose_name_plural = u"合同预览s"
		ordering = ['-id']  # id倒叙
		index_together = ["contract_type"]  # 索引字段组合
		permissions = (
			("browse_contractpreviewcode", u"浏览 合同预览"),
		)
