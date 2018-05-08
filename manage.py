#!/usr/bin/env python
import os
import sys
from modules.share_module.regular_tasks import *

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ace_office.settings")

	from django.core.management import execute_from_command_line

	if sys.argv[1] == "runserver":
		print "Start Time tasks ...."
	# all_tasks()

	execute_from_command_line(sys.argv)
