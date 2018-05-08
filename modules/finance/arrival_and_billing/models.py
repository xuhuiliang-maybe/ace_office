# coding=utf-8
import traceback

from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from modules.project_manage.models import Project

CREDITED_STATE = (
	('1', u'部分到账'),
	('2', u'全部到账'),
	('3', u'超额到账'),
	('4', u'未到账'),
)

Billing_STATE = (
	('1', u'部分开票'),
	('2', u'全部开票'),
	('3', u'超额开票'),
	('4', u'未开票'),
)


# 到账与开票
class ArrivalAndBilling(models.Model):
	project_name = models.ForeignKey(Project, verbose_name=u"项目名称", related_name="arrivalandbilling")
	settlement_date = models.DateField(u"结算月份")
	settlement_amount_long = models.PositiveIntegerField(u"结算金额（长期业务）", blank=True, null=True)
	settlement_amount_snap = models.PositiveIntegerField(u"结算金额（临时工）", blank=True, null=True)
	settlement_tatol = models.PositiveIntegerField(u"结算合计", blank=True, null=True)
	credited_amount_total = models.PositiveIntegerField(u"到账金额合计", blank=True, null=True)
	credited_date = models.DateField(u"到账时间", blank=True, null=True)
	credited_state = models.CharField(u"到账情况", choices=CREDITED_STATE, max_length=1, blank=True, null=True)
	billing_amount_total = models.PositiveIntegerField(u"开票金额合计", blank=True, null=True)
	billing_date = models.DateField(u"开票时间", blank=True, null=True)
	billing_state = models.CharField(u"开票情况", choices=Billing_STATE, max_length=1, blank=True, null=True)

	def __str__(self):
		return self.project_name.full_name

	class Meta:
		verbose_name = u"到账与开票"
		ordering = ['-id']  # id倒叙
		index_together = ["project_name"]  # 索引字段组合
		permissions = (
			("browse_arrivalandbilling", "浏览 到账与开票"),
			("export_arrivalandbilling", "导出 到账与开票"),
		)


# 到账明细
class CreditedDetails(models.Model):
	arrival = models.ForeignKey(ArrivalAndBilling, verbose_name=u"到账与开票", editable=False,
				    related_name="crediteddetails")
	credited_amount = models.PositiveIntegerField(u"到账金额", blank=True, null=True)
	credited_date = models.DateField(u"到账时间")

	def __str__(self):
		return str(self.credited_amount)

	class Meta:
		verbose_name = u"到账明细"
		ordering = ['-id']  # id倒叙


@receiver(post_save, sender=CreditedDetails)  # 信号的名字，发送者
def add_crediteddetails_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	"""新增/编辑 到账明细 保存事件 """
	try:
		credited_amount_total_sum = CreditedDetails.objects.filter(arrival=instance.arrival).aggregate(
			Sum('credited_amount'))
		credited_amount_sum = credited_amount_total_sum["credited_amount__sum"]
		credited_amount_total = 0
		if credited_amount_sum:
			credited_amount_total = credited_amount_sum

		ArrivalAndBilling.objects.filter(id=instance.arrival.id).update(
			credited_amount_total=credited_amount_total)
	except:
		traceback.print_exc()


@receiver(post_delete, sender=CreditedDetails)  # 信号的名字，发送者
def del_crediteddetails_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	""" 删除 到账明细 事件 """
	try:
		credited_amount_total_sum = CreditedDetails.objects.filter(arrival=instance.arrival).aggregate(
			Sum('credited_amount'))
		credited_amount_sum = credited_amount_total_sum["credited_amount__sum"]
		credited_amount_total = 0
		if credited_amount_sum:
			credited_amount_total = credited_amount_sum

		ArrivalAndBilling.objects.filter(id=instance.arrival.id).update(
			credited_amount_total=credited_amount_total)
	except:
		traceback.print_exc()


# 开票明细
class BillingDetails(models.Model):
	billing = models.ForeignKey(ArrivalAndBilling, verbose_name=u"到账与开票", editable=False,
				    related_name="billingdetails")
	billing_amount = models.PositiveIntegerField(u"开票金额", blank=True, null=True)
	billing_date = models.DateField(u"开票时间")

	def __str__(self):
		return str(self.billing_amount)

	class Meta:
		verbose_name = u"开票明细"
		ordering = ['-id']  # id倒叙


@receiver(post_save, sender=BillingDetails)  # 信号的名字，发送者
def add_billingdetails_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	"""新增/编辑 开票明细 保存事件 """
	try:
		billing_amount_total_sum = BillingDetails.objects.filter(billing=instance.billing).aggregate(
			Sum('billing_amount'))
		billing_amount_sum = billing_amount_total_sum["billing_amount__sum"]
		billing_amount_total = 0
		if billing_amount_sum:
			billing_amount_total = billing_amount_sum

		ArrivalAndBilling.objects.filter(id=instance.billing.id).update(
			billing_amount_total=billing_amount_total)
	except:
		traceback.print_exc()


@receiver(post_delete, sender=BillingDetails)  # 信号的名字，发送者
def del_billingdetails_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
	""" 删除 开票明细 事件 """
	try:
		billing_amount_total_sum = BillingDetails.objects.filter(billing=instance.billing).aggregate(
			Sum('billing_amount'))
		billing_amount_sum = billing_amount_total_sum["billing_amount__sum"]
		billing_amount_total = 0
		if billing_amount_sum:
			billing_amount_total = billing_amount_sum

		ArrivalAndBilling.objects.filter(id=instance.billing.id).update(
			billing_amount_total=billing_amount_total)
	except:
		traceback.print_exc()
