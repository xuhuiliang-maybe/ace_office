# coding=utf-8
import traceback

from django.core.cache import cache
from django.db import models

SYSVERSION = 1


class SystemConfig(models.Model):
	PARAMTYPECHOICE = (
		('1', u'常规'),
		('2', u'Email'),
		('3', u'定时任务'),
	)

	param_name = models.CharField(u"参数名", max_length=100)
	param_value = models.CharField(u"参数值", max_length=100)
	param_display = models.CharField(u"参数描述", max_length=100)
	param_type = models.CharField(u"参数类型", max_length=2, choices=PARAMTYPECHOICE)

	def __str__(self):
		return self.param_name + self.param_value

	class Meta:
		verbose_name = u"系统设置"
		index_together = ["id", "param_name"]  # 索引字段组合
		permissions = (
			("browse_systemconfig", u"浏览 系统设置"),
		)

	# 更新系统参数缓存
	def update_sysconfig_cache(self):
		global SYSVERSION
		SYSVERSION += 1

	@staticmethod
	def get_param(param_name):
		global SYSVERSION
		try:
			result = {param_name: ""}
			# sys_config = cache.get("sys_config_%s_%s" % (param_name, SYSVERSION))
			# if sys_config:
			# 	return sys_config
			sys_config = SystemConfig.objects.filter(param_name=param_name)
			if sys_config.exists():
				sys_config_s = sys_config[0]
				result = {sys_config_s.param_name: sys_config_s.param_value}
				cache.set("all_dept_%s_%s" % (param_name, SYSVERSION), result)
			return result
		except:
			traceback.print_exc()
			return {param_name: ""}

	def save(self, *args, **kwargs):
		global DEPTVERSION
		try:
			self.update_sysconfig_cache()
			super(SystemConfig, self).save(*args, **kwargs)
		except:
			traceback.print_exc()


STATUS_CHOICES = (
	('1', u'已备份'),
	('2', u'已还原'),
)


class DataBackup(models.Model):
	"""数据备份 """

	databasetype = models.CharField(u"数据库类型", max_length=256, blank=True)
	backupdatabase = models.CharField(u"备份文件名", max_length=256, blank=True)
	starttime = models.DateTimeField(u"备份开始时间", max_length=256, blank=True)
	endtime = models.DateTimeField(u"备份结束时间", max_length=256, blank=True)
	reduct_time = models.DateTimeField(u"还原时间", max_length=256, blank=True, null=True)
	status = models.CharField(u"状态", choices=STATUS_CHOICES, max_length=256, blank=True)
	operator = models.CharField(u"操作员", max_length=256, blank=True)

	remark1 = models.CharField(u"备注1", max_length=256, blank=True)
	remark2 = models.CharField(u"备注2", max_length=256, blank=True)
	remark3 = models.CharField(u"备注3", max_length=256, blank=True)
	remark4 = models.CharField(u"备注4", max_length=256, blank=True)
	remark5 = models.CharField(u"备注5", max_length=256, blank=True)

	def __str__(self):
		return self.databasetype + "-" + self.backupdatabase

	class Meta:
		verbose_name = u"数据备份"
		ordering = ['-id']  # id倒叙
		permissions = (
			("browse_databackup", u"浏览 数据库备份信息"),
			("reduct_databackup", u"还原 数据库备份信息"),
			("download_databackup", u"下载 数据库备份信息"),
		)

	def get_absolute_url(self):
		return "/system/data_backup"
