# coding=utf-8
from django import template
import traceback
import datetime
from django.utils import timezone
from modules.organizational_structure.departments.models import Department
from modules.system.models import SystemConfig

register = template.Library()

"""
1：字符串"true"转bool型True
2：字符串时间"2016-01-14"转datetime型时间
3：bool型True转字符串，是/否
"""


@register.filter
def bool_formater(bool_str=""):
	"""格式化字符串
	:param bool_str:字符串
	:return:True/False
	"""
	try:
		if bool_str == "true":
			return True
		if bool_str == "false":
			return False
		if not bool_str:
			return False
	except:
		traceback.print_exc()


@register.filter
def date_formater(date_str, formatstr):
	"""格式化时间
	:param date_str: "2016-01-14"
	:param formatstr: "%Y-%m-%d"
	:return:datetime型时间
	"""
	try:
		print date_str
		if date_str:
			return datetime.datetime.strptime(date_str, formatstr).replace(tzinfo=timezone.utc)
		else:
			return timezone.now()
	except:
		traceback.print_exc()


@register.filter
def true_false_formater(value):
	"""格式化为是/否
	:param value:bool型，
	:return: 是/否
	"""

	try:
		if value:
			return r'<i class="green ace-icon fa fa-check-circle bigger-130"></i>'
		return r'<i class="red ace-icon fa fa-times-circle bigger-130"></i>'
	except:
		traceback.print_exc()


@register.filter
def true_false_unformat(str_param):
	try:
		if str_param == u"是":
			return True
		if str_param == u"否":
			return False

	except:
		traceback.print_exc()
		return False


@register.filter
def get_parent_dept(id):
	try:
		if id:
			parent_dept = Department.get_dept_by_id(id)
			parent_dept_name = parent_dept.name
			return parent_dept_name
		return u"无"
	except:
		traceback.print_exc()
		return u"无"


@register.assignment_tag
def get_system_param(param_name):
	try:
		return SystemConfig.get_param(param_name).get(param_name, "")
	except:
		traceback.print_exc()
		return ""
