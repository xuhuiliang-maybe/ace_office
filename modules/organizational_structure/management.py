# coding=utf-8
import traceback

from django.db.models.signals import post_syncdb
from django.dispatch import receiver

from modules.organizational_structure import models as organizational_structure_app
from modules.organizational_structure.departments.models import Department


@receiver(post_syncdb, sender=organizational_structure_app)  # 信号的名字，发送者
def default_department(sender, **kwargs):  # 回调函数，收到信号后的操作
	"""初始化部门信息
	:param sender:
	:param kwargs:
	:return:
	"""
	try:
		default_department_obj = Department.objects.filter(parent_dept=0)
		if not default_department_obj.exists():
			department_obj = Department()
			department_obj.name = u"北京邦泰"
			department_obj.parent_dept = 0
			department_obj.save()
			print u"Init Department Info Success..."
	except:
		traceback.print_exc()

# """
# 在 django 中, 信号,主要有下面几类:
# 1.Model signals
#         1.pre_init
#         2.post_init
#         3.pre_save      在模型 save()方法调用之前或之后发送。
#         4.post_save
#         5.pre_delete    在模型delete()方法或查询集的delete() 方法调用之前或之后发送。
#         6.post_delete
#         7.class_prepared
#         8.m2m_changed   模型上的 ManyToManyField 修改时发送。
# 2.Management signals
#         1.post_syncdb   初始化数据库时发送。
# 3.Request/response signals
#         1.request_started   Django建立或关闭HTTP 请求时发送。
#         2.request_finished
#         3.got_request_exception
# 4.Test signals
#         1.template_rendered
# """
