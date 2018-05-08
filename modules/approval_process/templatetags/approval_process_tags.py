# coding=utf-8
from django import template
from django.core.urlresolvers import reverse

from modules.approval_process.models import *

register = template.Library()


@register.filter
def get_apply_details(pending_obj):
	"""
	:param obj:待审批对象
	:return:
	"""
	href_url = "#"
	try:
		model_name = pending_obj.content_type.natural_key()[1]
		reverse_str = 'approval:%s_one' % model_name
		view_type = "2"  # 1:由明细表返回，申请页面带查询条件，2：由待审批超链进去，不带查询条件
		href_url = reverse(reverse_str, args=(pending_obj.object_id, view_type))
	except:
		traceback.print_exc()
	finally:
		return href_url


@register.filter
def approval_title(apply_obj):
	try:
		style = {
			"1": "info",  # 请假
			"2": "pink",  # 备用金
			"3": "success",  # 报销与销账
			"4": "purple",  # 工资与职位调整
			"5": "yellow",  # 工资补发申请
			"6": "warning",  # 结算与发薪
			"7": "primary",  # 管理人员需求与离职
			"8": "grey",  # 临时工销账与开票
			"9": "inverse",  # 待招结算与销账
		}
		apply_type = apply_obj.apply_type
		return "<span class='label label-%s'>%s</span>" % (
			style[apply_type],
			apply_obj.get_apply_type_display()
		)
	except:
		traceback.print_exc()
		return ""


@register.filter
def approval_status(status_str):
	try:
		if status_str == "1":
			return "<span class='label label-danger arrowed-right arrowed-in'>待审批</span>"
		elif status_str == "2":
			return "<span class='label label-success arrowed-in arrowed-in-right'>通过</span>"
		elif status_str == "3":
			return "<span class='label arrowed arrowed-right'>拒绝</span>"
		else:
			return ""
	except:
		traceback.print_exc()


@register.filter
def get_start_date(event_object):
	try:
		event_model = event_object._meta.model_name
		if event_model == "leave":
			return event_object.begin_date
		elif event_model == "loan":
			return event_object.borrowing_date
		elif event_model == "wage":
			return u"无"
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_end_date(event_object):
	try:
		event_model = event_object._meta.model_name
		if event_model == "leave":
			return event_object.end_date
		elif event_model == "loan":
			return event_object.repayment_date
		elif event_model == "wage":
			return u"无"
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_loan_budget_details(obj):
	"""备用金，费用预算明细
	:param obj:
	:return:
	"""
	try:
		return obj.LoanBudgetDetails.count()
	except:
		traceback.print_exc()
		return 0


@register.filter
def get_write_offs_details(obj):
	"""报销与销账，明细
	:param obj:
	:return:
	"""
	try:
		return obj.WriteOffsDetails.count()
	except:
		traceback.print_exc()
		return 0


@register.filter
def get_wage_replacement_details(obj):
	"""报销与销账，明细
	:param obj:
	:return:
	"""
	try:
		return obj.WageReplacementDetails.count()
	except:
		traceback.print_exc()
		return 0


@register.filter
def format_difference(val):
	"""格式化，报销与销账 差额 字段
	已借备用金-报销/销账总额，结果如果是正数，自动显示出：应返还公司XX钱；如果是负数，自动显示：公司应支付XX钱
	:param val:
	:return:
	"""
	try:
		if val > 0:
			return "".join([u"应返还公司 ", str(val), u" 元"])
		elif val < 0:
			return "".join([u"公司应支付 ", str(val).split("-")[1], u" 元"])
		else:
			return val

	except:
		traceback.print_exc()


@register.filter
def get_recruitedbilling_details(obj):
	"""待招结算与销账，报销/销账明细
	:param obj:
	:return:
	"""
	try:
		return obj.RecruitedBillingDetails.count()
	except:
		traceback.print_exc()
		return 0


@register.filter
def get_temporarywriteoffsbillingdetails_count(obj):
	"""获取临时工销账与开票对应临时工信息
	:param obj:
	:return:
	"""
	try:
		return obj.temporarywriteoffsbillingdetails.count()
	except:
		traceback.print_exc()
		return 0
