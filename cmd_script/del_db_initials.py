# coding=utf-8
import fnmatch
import os
import traceback

"""
删除所有模块下，数据库迁移策略脚本
"""


def iterfindfiles(path, fnexp):
	try:
		for root, dirs, files in os.walk(path):
			for filename in fnmatch.filter(files, fnexp):
				yield os.path.join(root, filename)
	except:
		traceback.print_exc()


def del_file(root_path):
	try:
		for i in iterfindfiles(root_path, "*_initial.*"):
			print "delete ... ", i
			os.remove(i)
		for i in iterfindfiles(root_path, "*_auto_*.py"):
			print "delete ... ", i
			os.remove(i)
		for i in iterfindfiles(root_path, "000*.py"):
			print "delete ... ", i
			os.remove(i)
		for i in iterfindfiles(root_path, "*.pyc"):
			print "delete ... pyc ", i
			os.remove(i)
	except:
		traceback.print_exc()


if __name__ == '__main__':
	try:
		script_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		root_path = os.path.join(script_path, "modules")
		del_file(script_path)
		del_file(r"C:\Python27\Lib\site-packages\django\contrib\auth\migrations")
		print "finish ..."
		os.system("pause")
	except:
		traceback.print_exc()
