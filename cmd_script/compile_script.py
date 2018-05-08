# coding=utf-8
import compileall
import fnmatch
import os
import shutil
import sys
import traceback
from exceptions import KeyboardInterrupt


def iterfindfiles(path, fnexp):
	"""查找指定文件
	:param path:根路径
	:param fnexp:查找正则
	"""
	try:
		for root, dirs, files in os.walk(path):
			for filename in fnmatch.filter(files, fnexp):
				yield os.path.join(root, filename)
	except:
		traceback.print_exc()


def del_file(root_path):
	"""指定目录删除指定文件
	:param root_path:指定根目录
	"""
	try:
		for i in iterfindfiles(root_path, "*.py"):
			os.remove(i)
	except:
		traceback.print_exc()


def backups_and_compile(backup_dir):
	"""备份指定目录,并编译
	:param backup_dir: 需要编译的文件夹
	"""
	try:
		new_dir = "".join([backup_dir, "_bak_pyc"])
		if os.path.exists(new_dir):
			shutil.rmtree(new_dir)
		shutil.copytree(backup_dir, new_dir)
		compileall.compile_dir(new_dir)
		del_file(new_dir)
	except:
		traceback.print_exc()


def main():
	try:
		raw_input_package = raw_input("Input Need To Compile The Package: ")
		if raw_input_package and os.path.exists(raw_input_package):
			backups_and_compile(raw_input_package)
			print "Compiler success...."
		else:
			print "Cannot compile empty file: %s" % raw_input_package
			main()
		os.system("pause")
	except KeyboardInterrupt:
		sys.exit(0)


if __name__ == "__main__":
	main()
