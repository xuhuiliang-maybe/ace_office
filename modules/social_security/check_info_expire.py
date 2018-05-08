# coding=utf-8
import datetime
import traceback

from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from modules.social_security.increase_info.models import Increase
from modules.social_security.reduction_info.models import Reduction

"""
检查社保信息是否到期
兼容：增员信息，减员信息
到期只允许添加备注信息
"""


def comparison_time(check_in_time):
	"""比较时间大小，是否超期
	:param check_in_time:
	:return:True/False
	"""
	try:
		if not check_in_time:  # 增员日期为空，未到期
			return False
		now_date = datetime.date.today()
		if now_date > check_in_time:  # 系统时间大于增员时间，超期
			return True
	except:
		traceback.print_exc()


def get_increase_date(db_id, type, filed):
	social_obj = list()
	try:
		if type == "increase":
			social_obj = Increase.objects.filter(id=db_id)
		elif type == "reduction":
			social_obj = Reduction.objects.filter(id=db_id)

		if social_obj.exists():
			check_filed_date = ""
			employye_obj = social_obj[0].emplyid  # 社保信息对应员工

			if type == "increase":
				check_filed_date = employye_obj.social_insurance_increase_date  # 增员日期
			elif type == "reduction":
				check_filed_date = employye_obj.social_insurance_reduce_date  # 减员日期

			comparison_result = comparison_time(check_filed_date)  # 是否到期，系统日期大于登记时间
			return comparison_result
		return False
	except:
		traceback.print_exc()


def check_expire(function):
	# 查看是否到期
	def _wrapped_view(request, *args, **kwargs):
		db_id = kwargs.get("pk", "")  # 社保信息id
		request_url = request.META.get("PATH_INFO", "")  # 访问路径

		if "increase" in request_url:  # 社保福利，增员信息
			check_result = get_increase_date(db_id, "increase", "social_insurance_increase_date")
			if check_result:
				return redirect(reverse('increase_info:increase_edit_remark', args=(db_id,)))
		elif "reduction" in request_url:  # 社保福利，减员信息
			check_result = get_increase_date(db_id, "reduction", "social_insurance_increase_date")
			if check_result:
				return redirect(reverse('reduction_info:reduction_edit_remark', args=(db_id,)))

		return function(request, *args, **kwargs)

	return _wrapped_view
