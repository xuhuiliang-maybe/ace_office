# coding=utf-8
from django import template
from modules.approval_process.models import *
from django.utils import timezone

register = template.Library()


@register.filter
def get_status(end_time):
	try:
		is_invalid = timezone.now() > end_time
		if is_invalid:
			return "<span class='label label-danger arrowed-right arrowed-in'>失效</span>"
		else:
			return "<span class='label label-success arrowed-in arrowed-in-right'>有效</span>"
	except:
		traceback.print_exc()
