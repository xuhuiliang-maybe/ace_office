# coding=utf-8
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from ace_office import settings


@sensitive_post_parameters()
@csrf_protect
@never_cache
def user_login(request, template_name='login.html', redirect_field_name=REDIRECT_FIELD_NAME, current_app=None):
	"""显示登录表单和处理登录动作
	:param request:请求对象
	:param template_name:返回模板的名字
	:param redirect_field_name:重定向字段名
	:param current_app:当前应用程序
	:return:
	"""
	redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, '/'))
	remember_me = request.POST.get('remember_me', 0)
	username, password = "", ""
	if request.method == "POST":
		username = request.POST.get("username", "")
		password = request.POST.get("password", "")

		user = authenticate(username=username, password=password)
		print "login user==", user
		if user:
			print "is_staff==", user.is_staff
			print "is_active==", user.is_active
		if user and user.is_staff and user.is_active:
			# 确保用户始发重定向的网址是安全的。.
			if not is_safe_url(url=redirect_to, host=request.get_host()):
				redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
			# Okay, 安全检查完成，登录用户。
			else:
				login(request, user)
				# 检查是否保存
				if remember_me:
					expiry_time = 14 * 24 * 3600  # 14天后登陆超时
					request.session.set_expiry(expiry_time)

			return HttpResponseRedirect(redirect_to)
		elif user and not user.is_staff:
			messages.warning(request, u"您没有登录权限")
		elif user and not user.is_active:
			messages.warning(request, u"您已经离职，无登录权限")
		else:
			messages.warning(request, u"用户名或密码错误，登录失败")

	current_site = get_current_site(request)

	context = {
		redirect_field_name: redirect_to,
		'site': current_site,
		'site_name': current_site.name,
		"username": username,
		"password": password,
	}

	if current_app:
		request.current_app = current_app

	return TemplateResponse(request, template_name, context)


def user_logout(request):
	def go_back():
		# 管理后台登录
		if '/login' in request.META.get('HTTP_REFERER', ""):
			redirect_to = "/login/"
		# 其他
		else:
			redirect_to = '/'

		return HttpResponseRedirect(redirect_to)

	logout(request)

	return go_back()
