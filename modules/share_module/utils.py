# coding=utf-8
import traceback


# 获取动态查询条件
def get_kwargs(param):
	"""
	:param param:查询参数字典
	:return:
	"""
	kwargs = dict()
	try:
		[kwargs.update({query_field: param}) for query_field, param in param.items() if param]
	except:
		traceback.print_exc()
	finally:
		return kwargs
