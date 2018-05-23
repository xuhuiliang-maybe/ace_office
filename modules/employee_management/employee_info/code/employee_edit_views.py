# coding=utf-8
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.employee_management.employee_info.models import Employee, EmployeeForm
from modules.project_manage.models import Project
from modules.share_module.check_decorator import check_principal, check_user_is_songxiaodan
from modules.share_module.permissionMixin import class_view_decorator


# 员工信息-编辑
@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.change_employee', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
@class_view_decorator(check_user_is_songxiaodan)  # 校验是否是songxiaodan
class EmployeeUpdate(SuccessMessageMixin, UpdateView):
	template_name = "employee_edit.html"
	model = Employee
	form_class = EmployeeForm  # 自定义表单验证
	success_message = u"%(name)s 成功修改"

	def get_success_url(self):
		self.url = reverse('employee_info:list', args=("employee",))
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('employee_info:employee_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(EmployeeUpdate, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		context["form_content"] = u"修改员工信息"
		return context

	def form_valid(self, form):

		login_user = self.request.user

		# 非超级用户校验是否负责添加项目
		if not login_user.is_superuser:
			# 校验当前登录用户，不是录入项目的负责人是，阻止录入
			project_name = self.request.POST.get("project_name", "")  # 项目名称
			if not project_name:
				messages.warning(self.request, u"请选择您所负责的“项目名称”")
				return super(EmployeeUpdate, self).form_invalid(form)

			project_name = Project.objects.filter(id=project_name)
			principal = ""
			if project_name.exists():
				principal = project_name[0].principal
			if login_user != principal:
				messages.warning(self.request, u"请选择您所负责的“项目名称”")
				return super(EmployeeUpdate, self).form_invalid(form)

		# 校验身份证号，有在职员工有相同身份证号，不能同时存在，阻止录入，有相同身份证已离职可录入
		identity_card_number = self.request.POST.get('identity_card_number')
		status = self.request.POST.get('status')
		name = self.request.POST.get('name')
		user_obj = Employee.objects.filter(identity_card_number=identity_card_number, status="1").exclude(name=name)
		if user_obj.exists() and status == "1":
			# 身份证相同并在职，不予录入
			messages.warning(self.request, u"相同身份证号并且在职的员工信息已经存在!")
			return super(EmployeeUpdate, self).form_invalid(form)


		now_year = datetime.datetime.now().year
		id_card = self.request.POST.get("identity_card_number", "")
		age = self.request.POST.get("age", 0)
		if id_card and (age == "0" or not age):
			age_year_str = id_card[6:10]
			age = now_year - int(age_year_str)
		form.instance.age = int(age)

		# 计算性别
		sex = self.request.POST.get("sex", "")
		if id_card and not sex:
			sex_num = int(id_card[-2])
			if (sex_num % 2) == 0:
				sex = "F"
			else:
				sex = "M"
		form.instance.sex = sex

		return super(EmployeeUpdate, self).form_valid(form)


# 临时工信息－编辑
@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.change_temporary', raise_exception=True))
@class_view_decorator(check_principal)  # 校验是否负责该项目
class TemporaryUpdate(SuccessMessageMixin, UpdateView):
	template_name = "employee_edit.html"
	model = Employee
	success_message = u"%(name)s 成功修改"
	fields = [
		"name", "sex", "identity_card_number", "project_name",
		"recruitment_attache", "phone_number", "start_work_date", "end_work_date", "work_days", "hours",
		"amount_of_payment", "release_user", "release_time", "remark1",
	]

	def get_success_url(self):
		self.url = reverse('employee_info:list', args=("temporary",))
		referrer = self.request.POST.get("referrer", "")
		if referrer:
			self.url = referrer

		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('employee_info:temporary_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(TemporaryUpdate, self).get_context_data(**kwargs)
		context["form_content"] = u"修改临时工信息"
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def form_valid(self, form):

		# 校验当前登录用户，不是录入项目的负责人是，阻止录入
		login_user = self.request.user
		if not login_user.is_superuser:
			project_name = self.request.POST.get("project_name", "")  # 项目名称
			if not project_name:
				messages.warning(self.request, u"请选择您所负责的“项目名称”")
				return super(TemporaryUpdate, self).form_invalid(form)

			# 非超级用户校验是否负责添加项目
			project_name = Project.objects.filter(id=project_name)
			principal = ""
			if project_name.exists():
				principal = project_name[0].principal
			if login_user != principal:
				messages.warning(self.request, u"请选择您所负责的“项目名称”")
				return super(TemporaryUpdate, self).form_invalid(form)

		now_year = datetime.datetime.now().year
		id_card = self.request.POST.get("identity_card_number", "")
		age = self.request.POST.get("age", 0)
		if id_card and (age == "0" or not age):
			age_year_str = id_card[6:10]
			age = now_year - int(age_year_str)
		form.instance.age = int(age)

		# 计算性别
		sex = self.request.POST.get("sex", "")
		if id_card and not sex:
			sex_num = int(id_card[-2])
			if (sex_num % 2) == 0:
				sex = "F"
			else:
				sex = "M"
		form.instance.sex = sex

		return super(TemporaryUpdate, self).form_valid(form)
