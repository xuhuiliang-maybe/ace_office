# coding=utf-8
import calendar
import datetime
import traceback

from django.utils import timezone
from xlrd import xldate_as_tuple

"""
1：字符串"true"转bool型True
2：字符串时间"2016-01-14"转datetime型时间
3：bool型True转字符串，是/否
"""


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


def date_formater(date_str, formatstr):
	"""格式化时间
	:param date_str: "2016-01-14"
	:param formatstr: "%Y-%m-%d"
	:return:datetime型时间
	"""
	try:
		if date_str:
			return datetime.datetime.strptime(date_str, formatstr).replace(tzinfo=timezone.utc)
		else:
			return timezone.now()
	except:
		traceback.print_exc()


absent = {"0": u'否', "1": u'是'}


def true_false_formater(value):
	"""格式化为是/否
	:param value:bool型，
	:return: 是/否
	"""

	try:
		if value:
			return absent['1']
		return absent['0']
	except:
		traceback.print_exc()


def true_false_unformat(str_param):
	try:
		if not str_param:
			return False
		if str_param == u"是" or str_param == u"在职":
			return True
		if str_param == u"否" or str_param == u"离职":
			return False

	except:
		traceback.print_exc()
		return False


def true_false_unformat_new(str_param):
	result = '2'
	try:
		if str_param == u"是":
			result = '1'
		if str_param == u"否":
			result = '2'
	except:
		traceback.print_exc()
	finally:
		return result


def get_excel_date(date_str, date_joined=False):
	try:
		if date_str:
			return datetime.datetime(*xldate_as_tuple(date_str, 0))
		if date_joined:
			return timezone.now()
		return None
	except:
		traceback.print_exc()
		try:
			return datetime.datetime.strptime(date_str, "%Y-%m-%d")
		except:
			traceback.print_exc()
		return None


def get_excel_int(param_str, none=False):
	try:
		if param_str:
			return int(param_str)
		if none:
			return ""
		return 0
	except:
		traceback.print_exc()
		return 0


def get_excel_float(param_str):
	try:
		if param_str:
			return float(param_str)
		return 0
	except:
		return 0


def add_months(dt, months):
	month = dt.month - 1 + months
	year = dt.year + month / 12
	month = month % 12 + 1
	day = min(dt.day, calendar.monthrange(year, month)[1])
	return dt.replace(year=year, month=month, day=day)
