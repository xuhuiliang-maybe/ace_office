# coding=utf-8
import os
import traceback

from ace_office.settings import MEDIA_ROOT, BASE_DIR


def get_media_sub_path(foldername=""):
	"""获取软件media目录下指定子目录"""
	try:
		return os.path.join(MEDIA_ROOT, foldername)
	except:
		traceback.print_exc()


if __name__ == "__main__":
	test_path = get_media_sub_path("mysql_backup/")
	print test_path
	print MEDIA_ROOT
	print BASE_DIR
