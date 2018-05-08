# coding=utf-8
from django import template
import traceback

register = template.Library()


@register.filter
def selectgender(value):
	"""格式化为是/否
	:param value:M/F，
	:return: 男/女
	"""

	absent = {"M": u'男', "F": u'女'}
	try:
		if value:
			return absent[value]
		return ""
	except:
		traceback.print_exc()
