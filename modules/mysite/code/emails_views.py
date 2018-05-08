# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext


@login_required()
def emails_list(request):
	"""网站主页
	:param request:
	:return:
	"""
	return render_to_response('email_info.html', {}, context_instance=RequestContext(request))

