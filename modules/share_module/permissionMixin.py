# coding=utf-8
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


# class LoginRequiredMixin(object):
# 	"""是否允许登录的网站用户"""
#
# 	@method_decorator(user_passes_test(lambda u: u.is_staff, login_url="/accounts/login"))
# 	def dispatch(self, *args, **kwargs):
# 		return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class MustBeSuperUserMixin(object):
	""" 是否超级管理员 """

	@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url="/accounts/login"))
	def dispatch(self, *args, **kwargs):
		return super(MustBeSuperUserMixin, self).dispatch(*args, **kwargs)


def class_view_decorator(function_decorator):
	"""Convert a function based decorator into a class based decorator usable
	on class based Views.
	Can't subclass the `View` as it breaks inheritance (super in particular),
	so we monkey-patch instead.
	"""

	def simple_decorator(view):
		view.dispatch = method_decorator(function_decorator)(view.dispatch)
		return view

	return simple_decorator
