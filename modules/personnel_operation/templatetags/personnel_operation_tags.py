# coding=utf-8
import datetime
import traceback

from django import template
from django.db.models import Sum

from modules.personnel_operation.models import QualityAssurance
from modules.project_manage.models import Project

register = template.Library()


@register.filter
def compute_use_days(personnel):
	"""计算已用天数
	1/如果”改善状态”字段是“改善“，则等于改善日期-问题日期
	2/如果"改善状态”字段是“持续“，则等于当前日期-问题日期
	:param personnel:个人操作质量单条数据对象
	:return:天数
	"""
	use_day = 0
	try:
		now_date = datetime.date.today()  # 现在日期
		improve_status = personnel.improve_status.name  # 改善状态
		improve_date = personnel.improve_date  # 改善日期
		error_date = personnel.error_date  # 问题日期
		if improve_status == u"改善":
			use_day = (improve_date - error_date).days
		else:
			use_day = (now_date - error_date).days
	except:
		traceback.print_exc()
	return use_day


@register.filter
def compute_extended_error(personnel):
	"""超期错误数
	改善日期-（问题日期+改善时限）
	:param personnel:
	:return:
	"""
	extended_error_num = 0
	try:
		improve_date = personnel.improve_date  # 改善日期
		error_date = personnel.error_date  # 问题日期
		improve_time = personnel.improve_time  # 改善时限
		extended_error_num = (improve_date - error_date).days - improve_time
	except:
		traceback.print_exc()
	return extended_error_num


@register.filter
def compute_total_error(personnel):
	"""错误合计
	操作错误数+超期错误数
	:param personnel:
	:return:
	"""
	total = 0
	try:
		error_number = personnel.error_number  # 操作错误数
		improve_date = personnel.improve_date  # 改善日期
		error_date = personnel.error_date  # 问题日期
		improve_time = personnel.improve_time  # 改善时限
		extended_error_num = (improve_date - error_date).days - improve_time
		total = error_number + extended_error_num
	except:
		traceback.print_exc()
	return total


@register.filter
def get_project_principal(project_param):
	"""操作汇总-获取项目负责人
	:param project_param:{'project_id': 2}
	:return:
	"""
	try:
		kwargs = {"id": project_param["project_id"]}
		project_obj = Project.objects.get(**kwargs)
		return project_obj.principal
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_department(project_param):
	"""操作汇总-获取部门名称
	:param project_param:{'project_id': 2}
	:return:
	"""
	try:
		return QualityAssurance.objects.filter(**project_param).first().department.name
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_error_number(project_param):
	"""操作汇总-操作错误数-合计
	:param project_param:{'project_id': 2}
	:return:
	"""
	try:
		sum_error_number = QualityAssurance.objects.filter(**project_param).aggregate(Sum('error_number'))
		return sum_error_number["error_number__sum"]
	except:
		traceback.print_exc()
		return 0


@register.filter
def get_compute_extended_error(project_param):
	"""操作汇总-获取超期错误数-合计
	:param project_param:{'project_id': 2}
	:return:
	"""
	try:
		all_obj = QualityAssurance.objects.filter(**project_param)
		return sum([compute_extended_error(one) for one in all_obj])
	except:
		traceback.print_exc()
		return 0


@register.filter
def get_compute_total_error(project_param):
	"""操作汇总-获取错误合计
	:param project_param:{'project_id': 2}
	:return:
	"""
	try:
		all_obj = QualityAssurance.objects.filter(**project_param)
		return sum([compute_total_error(one) for one in all_obj])
	except:
		traceback.print_exc()
		return 0
