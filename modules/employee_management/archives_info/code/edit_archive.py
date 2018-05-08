# coding=utf-8
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.employee_management.employee_info.models import Archive
from modules.share_module.check_decorator import check_principal
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.change_archive', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class ArchiveUpdate(SuccessMessageMixin, UpdateView):
	model = Archive
	template_name = "archive_edit.html"
	success_message = u"成功修改"
	fields = [
		"number",
		"type",
		"issue",
		"receive",
		"bank_copy",
		"id_copy",
		"booklet_copy",
		"photo",
		"contract",
		"resume",
		"family_contract",
		"entry_conditions",
		"breach_book",
		"salary_confirmation",
		"health_certificate",
		"his_resignation",
		"labor_relations_prove",
		"register_letter",
		"relieve_letter",
	]

	def get_success_url(self):
		self.url = reverse('archive_info:archive_list', args=())
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		return self.url

	def get_context_data(self, **kwargs):
		context = super(ArchiveUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改员工档案信息"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def form_valid(self, form):
		login_user = self.request.user
		pk = self.kwargs.get("pk", "")
		new_receive = self.request.POST.get("receive", "")  # 是否收到
		new_number = self.request.POST.get("number", "")  # 档案编号

		# 修改档案信息【是否收到】字段，必须由档案专员操作,超级用户除外
		try:
			archive_obj = Archive.objects.values("receive", "number").filter(id=pk)
			old_receive = archive_obj[0].get("receive", "")
			old_number = archive_obj[0].get("number", "")
			if new_receive != old_receive:  # 对是否收到做编辑
				if login_user.position != u"档案专员" and not login_user.is_superuser:
					messages.warning(self.request, u"【是否收到】只能由【档案专员】做确认！")
					return super(ArchiveUpdate, self).form_invalid(form)
			elif new_number != old_number:
				if login_user.position != u"档案专员" and not login_user.is_superuser:
					messages.warning(self.request, u"【档案编号】只能由【档案专员】做确认！")
					return super(ArchiveUpdate, self).form_invalid(form)
		except:
			traceback.print_exc()
			messages.warning(self.request, u"【是否收到】只能由【档案专员】做确认！")
			return super(ArchiveUpdate, self).form_invalid(form)

		return super(ArchiveUpdate, self).form_valid(form)
