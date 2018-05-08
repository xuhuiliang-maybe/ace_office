# coding=utf-8
from django.test import TestCase
from django.core.cache import cache
from modules.organizational_structure.departments.models import DEPTVERSION

"""
执行：python manage.py test ace_office
"""


class MemcachedTestCase(TestCase):
	"""缓存相关 """

	def setUp(self):
		pass

	def update_cache(self):
		global DEPTVERSION
		DEPTVERSION += 1

	def test_memcached(self):
		# 取缓存中的数据
		param_a = cache.get("param_a")
		print "memcache get param_a ==", param_a

		# 设置缓存
		cache.set("param_b", 111)
		param_b = cache.get("param_b")
		print "memcache get param_b ==", param_b

		# 删除缓存
		cache.delete("param_b")
		param_b = cache.get("param_b")
		print "memcache get param_b ==", param_b

		# 更新缓存, 改变全局变量，改变索引名实现更新
		cache.set("param_c_%s" % DEPTVERSION, 222)
		print "update befor get param_c", cache.get("param_c_%s" % DEPTVERSION)
		self.update_cache()
		print "update after get param_c", cache.get("param_c_%s" % DEPTVERSION)
