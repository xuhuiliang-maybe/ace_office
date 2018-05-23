# coding=utf-8
import datetime
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.employee_management.employee_info.models import Employee, EmployeeForm
from modules.project_manage.models import Project
from modules.share_module.permissionMixin import class_view_decorator


# 新增员工信息
@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.add_employee', raise_exception=True))
class EmployeeCreate(SuccessMessageMixin, CreateView):
	template_name = "employee_edit.html"
	form_class = EmployeeForm
	model = Employee
	success_message = u"%(name)s 成功创建"

	def get_success_url(self):
		self.url = reverse('employee_info:list', args=("employee",))
		# referrer = self.request.POST.get("referrer", "")
		# if referrer:
		# 	self.url = referrer
		_addanother = self.request.POST.get("_addanother", "")
		if _addanother:
			self.url = reverse('employee_info:employee_add')
		return self.url

	def get_context_data(self, **kwargs):
		context = super(EmployeeCreate, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def form_valid(self, form):
		try:
			# 校验当前登录用户，不是录入项目的负责人是，阻止录入
			login_user = self.request.user
			project_name = self.request.POST.get("project_name", 0)  # 项目名称
			if not project_name:
				messages.warning(self.request, u"请选择您所负责的“项目名称”")
				return super(EmployeeCreate, self).form_invalid(form)

			# 非超级用户校验是否负责添加项目
			if not login_user.is_superuser:
				project_name = Project.objects.filter(id=project_name)
				principal = ""
				if project_name.exists():
					principal = project_name[0].principal
				if login_user != principal:
					messages.warning(self.request, u"请选择您所负责的“项目名称”")
					return super(EmployeeCreate, self).form_invalid(form)

			# 校验身份证号，有在职员工有相同身份证号，不能同时存在，阻止录入，有相同身份证已离职可录入
			identity_card_number = self.request.POST.get('identity_card_number')
			status = self.request.POST.get('status')
			user_obj = Employee.objects.filter(identity_card_number=identity_card_number, status="1")
			if user_obj.exists() and status == "1":
				# 身份证相同并在职，不予录入
				messages.warning(self.request, u"相同身份证号并且在职的员工信息已经存在!")
				return super(EmployeeCreate, self).form_invalid(form)

			# 根据身份证号计算年龄
			now_year = datetime.datetime.now().year
			id_card = self.request.POST.get("identity_card_number", "")  # 身份证号
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
		except:
			traceback.print_exc()

		return super(EmployeeCreate, self).form_valid(form)


# 新增临时工信息
@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.add_temporary', raise_exception=True))
class TemporaryCreate(SuccessMessageMixin, CreateView):
	model = Employee
	template_name = "employee_edit.html"
	success_message = u"%(name)s 成功创建"
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
		context = super(TemporaryCreate, self).get_context_data(**kwargs)
		referrer = self.request.META.get('HTTP_REFERER', "")
		context["referrer"] = referrer
		return context

	def form_valid(self, form):
		try:
			form.instance.is_temporary = True
			# 校验当前登录用户，不是录入项目的负责人是，阻止录入
			login_user = self.request.user
			project_name = self.request.POST.get("project_name", 0)  # 项目名称
			if not project_name:
				messages.warning(self.request, u"请选择您所负责的“项目名称”")
				return super(TemporaryCreate, self).form_invalid(form)

			# 非超级用户校验是否负责添加项目
			if not login_user.is_superuser:
				project_name = Project.objects.filter(id=project_name)
				principal = ""
				if project_name.exists():
					principal = project_name[0].principal
				if login_user != principal:
					messages.warning(self.request, u"请选择您所负责的“项目名称”")
					return super(TemporaryCreate, self).form_invalid(form)

			# 根据身份证号计算年龄
			now_year = datetime.datetime.now().year
			id_card = self.request.POST.get("identity_card_number", "")  # 身份证号
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
		except:
			traceback.print_exc()

		return super(TemporaryCreate, self).form_valid(form)
