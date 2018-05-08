# coding=utf-8
import traceback

from django.db.models.signals import post_syncdb
from django.dispatch import receiver

from modules.system import models as system_app
from modules.system.models import SystemConfig


@receiver(post_syncdb, sender=system_app)
def init_dict_table_info(sender, **kwargs):
	"""初始化字典表
	:param sender:
	:param kwargs:
	:return:
	"""
	try:
		init_param_list = [
			{"param_name": "site_name", "param_value": "Ace Office", "param_display": u"系统名称",
			 "param_type": "1"},
			{"param_name": "company_name", "param_value": u"公司", "param_display": u"公司名称",
			 "param_type": "1"},
			{"param_name": "scheduled_backup", "param_value": "0", "param_display": u"备份数据库间隔(天)",
			 "param_type": "3"},
			{"param_name": "scheduled_clean", "param_value": "0", "param_display": u"清理数据库备份间隔(天)",
			 "param_type": "3"},
		]
		for kwargs in init_param_list:
			systemconfig_obj = SystemConfig.objects.filter(param_name=kwargs["param_name"])
			if not systemconfig_obj.exists():
				SystemConfig.objects.get_or_create(**kwargs)
		print "init system config success..."
	except:
		traceback.print_exc()
