# coding=utf-8
import traceback
from django.db.models import Sum
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from modules.approval_process.loan.models import Loan
from modules.approval_process.models import PendingApproval
from modules.approval_process.models import Public
from modules.dict_table.models import Subject
from modules.finance.loans_and_write_offs.models import LoansAndWriteOffs
from modules.organizational_structure.departments.models import Department
from modules.middleware import threadlocals

WRITEOFFS_TYPE = (
	('1', u'票据销账'),
	('2', u'结算销账'),
	('3', u'其他销账'),
)


class WriteOffs(Public):
	""" 报销与销账 """
	handle_user = models.ForeignKey(User, verbose_name=u"审批人", related_name="writeoffs_handle_user", blank=True,
					null=True)
	apply_user = models.ForeignKey(User, verbose_name=u"申请人", related_name="writeoffs_apply_user")

	writeoffs_total = models.PositiveIntegerField(u"报销/销账总额", default=0, editable=False)
	borrow_imprest = models.PositiveIntegerField(u"已借备用金", default=0)
	imprest_explain = models.CharField(u"备用金说明", max_length=256, blank=True, null=True)

	# 已借备用金-报销/销账总额，结果如果是正数，自动显示出：应返还公司XX钱；如果是负数，自动显示：公司应支付XX钱
	difference = models.PositiveIntegerField(u"差额", default=0, editable=False)
	writeoffs_type = models.CharField(u"销账类型", choices=WRITEOFFS_TYPE, max_length=1, blank=True, null=True)
	remark = models.CharField(u"备注", max_length=256, blank=True, null=True)

	def __str__(self):
		return self.title + "-" + self.note

	class Meta:
		verbose_name = u"报销与销账"
		ordering = ['-id']  # id倒叙
		index_together = ["title", "apply_user"]  # 索引字段组合
		permissions = (
			("browse_write_offs", u"浏览 报销与销账"),
		)


class WriteOffsForm(forms.ModelForm):
	borrow_imprest = forms.ChoiceField(label=u'已借备用金')

	def __init__(self, *args, **kwargs):
		super(WriteOffsForm, self).__init__(*args, **kwargs)

		# 组装已借备用金，从相同月份的社保明细和薪资汇总明细中的所有身份证号码不重复地显示出来
		login_user = threadlocals.get_current_user()  # 获取登录用户
		loan_list = Loan.objects.filter(apply_user=login_user)  # 当前用户借款申请

		# 当前用户，财务管理－借款与销账，已销账
		loansandwriteoffs = LoansAndWriteOffs.objects.filter(loan__in=loan_list, amount_write_offs__gt=0,
								     write_offs_date__isnull=False).values_list("loan",
														flat=True)

		loan_list = loan_list.exclude(id__in=list(loansandwriteoffs))  # 将已销账排除

		loan_list = list(loan_list.values_list("money", flat=True))  # 获取已排除  已销账借款信息
		self.fields['borrow_imprest'].choices = ((x, x) for x in loan_list)

	class Meta:
		model = WriteOffs
		fields = ["title", "note", "borrow_imprest", "imprest_explain", "writeoffs_type", "remark"]


@receiver(post_save, sender=WriteOffs)  # 信号的名字，发送者
def add_writeoffs_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	"""增加 报销与销账 申请事件 """
	try:
		pend_obj = PendingApproval.objects.filter(object_id=instance.id, apply_type="3")
		if not pend_obj.exists():
			PendingApproval(event=instance, apply_type="3").save()
	except:
		traceback.print_exc()


COST_SHARING_CHOICE = (
	("1", "项目分摊"),
	("2", "部门分摊"),
	("3", "公司分摊"),
)


class WriteOffsDetails(models.Model):
	"报销/销账，明细表"
	applicants = models.ForeignKey(WriteOffs, verbose_name=u"报销/销账申请", editable=False,
				       related_name="WriteOffsDetails")

	date_range = models.DateField(u"日期")
	money = models.PositiveIntegerField(u"金额", default=0)
	subject = models.ForeignKey(Subject, verbose_name=u"科目")
	department = models.ForeignKey(Department, verbose_name=u"费用部门")
	project_name = models.CharField(u"费用项目", max_length=255, blank=True, null=True)
	cost_sharing = models.CharField(u"费用分摊方式", max_length=1, choices=COST_SHARING_CHOICE)
	cost_detail = models.TextField(u"费用明细说明")
	invoice_situation = models.TextField(u"发票情况")
	payee = models.ForeignKey(User, verbose_name=u"领款人", related_name="writeoffsdetail_payee")
	remark = models.CharField(u"备注", max_length=256, null=True, blank=True)

	def __str__(self):
		return str(self.date_range)

	class Meta:
		verbose_name = u"报销与销账，明细表"


@receiver(post_save, sender=WriteOffsDetails)  # 信号的名字，发送者
def add_write_offs_details_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	"""新增/编辑 报销与销账明细 保存事件 """
	try:
		# 修改报销与销账-明细后，
		# 重新计算报销与销账总额和差额
		writeoffs_obj = WriteOffs.objects.filter(id=instance.applicants.id)
		writeoffs_total_sum = WriteOffsDetails.objects.filter(applicants=writeoffs_obj).aggregate(Sum('money'))
		money_sum = writeoffs_total_sum["money__sum"]
		writeoffs_total = 0
		if money_sum:
			writeoffs_total = money_sum

		# 计算差额
		# 已借备用金
		borrow_imprest_list = WriteOffs.objects.filter(id=instance.applicants.id).values_list("borrow_imprest",
												      flat=True)
		if borrow_imprest_list:
			borrow_imprest = borrow_imprest_list[0]
		else:
			borrow_imprest = 0
		difference = int(borrow_imprest) - writeoffs_total

		WriteOffs.objects.filter(id=instance.applicants.id).update(writeoffs_total=writeoffs_total,
									   difference=difference)
	except:
		traceback.print_exc()


@receiver(post_delete, sender=WriteOffsDetails)  # 信号的名字，发送者
def del_write_offs_details_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	""" 删除 报销与销账明细 事件 """
	try:
		# 修改报销与销账-明细后，
		# 重新计算报销与销账总额和差额
		writeoffs_obj = WriteOffs.objects.filter(id=instance.applicants.id)
		writeoffs_total_sum = WriteOffsDetails.objects.filter(applicants=writeoffs_obj).aggregate(Sum('money'))
		money_sum = writeoffs_total_sum["money__sum"]
		writeoffs_total = 0
		if money_sum:
			writeoffs_total = money_sum

		# 计算差额
		# 已借备用金
		borrow_imprest_list = WriteOffs.objects.filter(id=instance.applicants.id).values_list("borrow_imprest",
												      flat=True)
		if borrow_imprest_list:
			borrow_imprest = borrow_imprest_list[0]
		else:
			borrow_imprest = 0
		difference = int(borrow_imprest) - writeoffs_total

		WriteOffs.objects.filter(id=instance.applicants.id).update(writeoffs_total=writeoffs_total,
									   difference=difference)
	except:
		traceback.print_exc()
