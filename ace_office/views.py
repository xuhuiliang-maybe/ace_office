# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext


# 链接指向的网页不存在
def redirect_404_error(request):
	return render_to_response('error/404.html', {}, context_instance=RequestContext(request))


# 服务器内部错误
def redirect_500_error(request):
	return render_to_response('error/500.html', {}, context_instance=RequestContext(request))


# 无权限请求
def redirect_403_error(request):
	return render_to_response('error/403.html', {}, context_instance=RequestContext(request))


# 请求出错
def redirect_400_error(request):
	return render_to_response('error/400.html', {}, context_instance=RequestContext(request))
