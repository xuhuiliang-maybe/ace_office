# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.approval_process.wage.models import Wage
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('wage.add_wage', raise_exception=True))
class WageCreate(SuccessMessageMixin, CreateView):
	template_name = "base/document_edit.html"
	model = Wage
	fields = ["title", "note", "money"]
	success_message = u"%(title)s 成功申请"

	def get_success_url(self):
		self.url = reverse('approval:wage_list', args=())
		referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('approval:wage_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(WageCreate, self).get_context_data(**kwargs)
		context["form_content"] = u"工资申请"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	# 将登陆用户作为申请人
	def form_valid(self, form):
		form.instance.apply_user = self.request.user
		form.instance.apply_types = "4"
		return super(WageCreate, self).form_valid(form)
