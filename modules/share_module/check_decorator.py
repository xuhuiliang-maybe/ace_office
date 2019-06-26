# coding=utf-8
import traceback

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse

from ace_office import settings
from config.conf_core import SUPERUSERNAMES
from modules.approval_process.loan.models import LoanBudgetDetails
from modules.approval_process.recruited_billing.models import RecruitedBillingDetails
from modules.approval_process.temporary_write_offs_billing.models import TemporaryWriteOffsBillingDetails
from modules.approval_process.wage_replacement.models import WageReplacementDetails
from modules.approval_process.write_offs.models import WriteOffsDetails
from modules.employee_management.employee_info.models import Archive
from modules.employee_management.employee_info.models import Employee
from modules.expense_manage.models import Expense
from modules.personnel_operation.models import QualityAssurance
from modules.project_manage.models import Project
from modules.settlement_pay.models import Payroll
from modules.social_security.increase_info.models import Increase
from modules.social_security.reduction_info.models import Reduction


# 审批相关，校验是否已审批
def check_is_approval(function):
	def _wrapped_view(request, *args, **kwargs):
		db_id = kwargs.get("pk", "")
		model_name = kwargs.get("model_name", "")
		try:
			# 临时工销账与开票：明细，备用金：费用预算明细，报销与销账：明细表，工资补发申请：补发明细
			if model_name == TemporaryWriteOffsBillingDetails or model_name == LoanBudgetDetails or model_name == WriteOffsDetails or model_name == WageReplacementDetails or model_name == RecruitedBillingDetails:
				obj = model_name.objects.filter(id=db_id)
				if obj.exists():
					if obj[0].applicants.status != "1":
						messages.warning(request, u"审配状态不是 待审批 状态！")
						raise PermissionDenied
			else:
				status = model_name.objects.values("status").filter(id=db_id)
				if status.exists():
					if status[0].get("status", "") != "1":
						messages.warning(request, u"审配状态不是 待审批 状态！")
						raise PermissionDenied
		except:
			# 没有项目负责人信息
			traceback.print_exc()
			messages.warning(request, u"没有项目负责人信息！")
			raise PermissionDenied
		return function(request, *args, **kwargs)

	return _wrapped_view


# 是否是songxiaodna
def check_user_is_songxiaodan(function):
	def _wrapped_view(request, *args, **kwargs):
		login_user = request.user
		db_id = kwargs.get("pk", "")  # 员工信息id
		model_name = kwargs.get("model_name", "")
		try:
			model_obj = model_name.objects.filter(id=db_id)
			if model_obj.exists():
				if login_user.username not in SUPERUSERNAMES and model_obj.first().status in ["2", "3"]:
					messages.warning(request, u"员工'目前状态'为'离职、调出'时，只能由'%s'维护信息！" % ",".join(SUPERUSERNAMES))
					raise PermissionDenied
		except:
			# 没有项目负责人信息
			traceback.print_exc()
			messages.warning(request, u"没有项目负责人信息！")
			raise PermissionDenied
		return function(request, *args, **kwargs)

	return _wrapped_view

def check_principal(function):
	"""是否负责该项目
	:param function:
	:return:
	"""
	def _wrapped_view(request, *args, **kwargs):
		login_user = request.user
		db_id = kwargs.get("pk", "")  # 员工信息id
		model_name = kwargs.get("model_name", "")
		try:
			model_obj = model_name.objects.filter(id=db_id)
			if model_obj.exists():
				if not login_user.is_superuser and not login_user.dept_head:
					if model_name == Archive:  # 档案信息
						if model_obj[0].employee_id.project_name.principal != login_user:
							messages.warning(request, u"不是项目负责人！")
							raise PermissionDenied
					elif model_name == Expense or model_name == Increase or model_name == Reduction:  # 费用管理, 增员，减员
						if model_obj[0].emplyid.project_name.principal != login_user:
							messages.warning(request, u"不是项目负责人！")
							raise PermissionDenied
					elif model_name == QualityAssurance:  # 个人操作质量
						if model_obj[0].project_id.principal != login_user:
							messages.warning(request, u"不是项目负责人！")
							raise PermissionDenied
					elif model_name == Project:  # 项目信息
						if model_obj[0].principal != login_user:
							messages.warning(request, u"不是项目负责人！")
							raise PermissionDenied
					elif model_name == Payroll:  # 结算发薪
						if model_obj[0].employee.project_name.principal != login_user:
							messages.warning(request, u"不是项目负责人！")
							raise PermissionDenied
					else:
						# 员工信息
						if model_obj[0].project_name.principal != login_user:
							messages.warning(request, u"不是项目负责人！")
							raise PermissionDenied
		except:
			# 没有项目负责人信息
			traceback.print_exc()
			messages.warning(request, u"没有项目负责人信息！")
			raise PermissionDenied
		return function(request, *args, **kwargs)

	return _wrapped_view


# 校验是否有此员工
def check_employee(function):
	def _wrapped_view(request, *args, **kwargs):
		name = request.GET.get("name")
		identity_card_number = request.GET.get("identity_card_number")
		emp_obj = Employee.objects.filter(name=name, identity_card_number=identity_card_number)
		if not emp_obj.exists():
			redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
			messages.warning(request, u"您还不是合法员工！")
			# return HttpResponseRedirect(redirect_to)
			return TemplateResponse(request, "login.html", {"target": "#signup-box"})
		return function(request, *args, **kwargs)

	return _wrapped_view
