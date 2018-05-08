# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.contract_manage.models import *
from modules.contract_manage.service.service_forms import ContractServiceForm
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('contract_manage.change_contractservice', raise_exception=True))
class ContractServiceUpdate(SuccessMessageMixin, UpdateView):
	model = ContractService
	form_class = ContractServiceForm
	template_name = "contract_edit.html"
	success_message = u"%(name)s 成功修改"

	def get_context_data(self, **kwargs):
		context = super(ContractServiceUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"合同签订-劳务"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def get_success_url(self):
		self.url = reverse('contract:list_service', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('contract:add_service')
		return self.url

	def form_valid(self, form):
		receive_address = self.request.POST.get("receive_address", "")  # 指定通知接收地址
		address = self.request.POST.get("address", "")  # 住址
		deadline = self.request.POST.get("deadline", "")  # 合同期限
		start_date = self.request.POST.get("start_date", "")  # 合同开始时间
		end_date = self.request.POST.get("end_date", "")  # 合同结束时间

		# 计算-指定通知接收地址
		if not receive_address:
			if address:
				form.instance.receive_address = address

		# 计算-试用期
		form.instance.probation = deadline

		# 计算-合同结束时间
		if not end_date:
			if deadline and start_date:
				start_date_datetime = datetime.datetime.strptime(start_date, "%Y/%m/%d")

				if deadline == "1":  # 24个月
					end_date = add_months(start_date_datetime, 24)
				if deadline == "2":  # 36个月
					end_date = add_months(start_date_datetime, 36)
				form.instance.end_date = end_date
		return super(ContractServiceUpdate, self).form_valid(form)
